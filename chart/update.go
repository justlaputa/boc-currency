package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"math/big"
	"net/http"
	"os"
	"time"

	"cloud.google.com/go/bigquery"
	"cloud.google.com/go/storage"
	"gocloud.dev/blob"
	"google.golang.org/api/iterator"

	//use gcs
	_ "gocloud.dev/blob/gcsblob"
)

//Config application config data
type Config struct {
	GoogleProjectID   string
	BQDataset         string
	BQTable           string
	BucketURL         string
	DataFileObjectKey string
}

//ExchangeRateRecord export as json
type ExchangeRateRecord struct {
	Timestamp   time.Time `json:"timestamp"`
	ExchangeBuy float64   `json:"ex_buy"`
	Middle      float64   `json:"middle"`
}

//ExchangeRateData exchange rate data as an array of all rate records
type ExchangeRateData []ExchangeRateRecord

func main() {
	config := loadConfig()

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		data, err := getExchangeRateData(config)
		if err != nil {
			fmt.Printf("failed to get exchange rate data from bigquery: %v\n", err)
			w.WriteHeader(http.StatusInternalServerError)
			return
		}

		fmt.Printf("got %d records from bigquery\n", len(data))

		err = updateRemoteFile(data, config)
		if err != nil {
			fmt.Printf("failed to save data to remote storage: %v\n", err)
			w.WriteHeader(http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "success")
	})

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("starting chart updater on: %s", port)

	log.Fatal(http.ListenAndServe(":"+port, nil))

}

func loadConfig() *Config {
	result := &Config{}

	result.GoogleProjectID = getEnvOrDie("GOOGLE_PROJECT_ID")
	result.BQDataset = getEnvOrDie("CURRENCY_RATE_DATASET")
	result.BQTable = getEnvOrDie("CURRENCY_RATE_TABLE")
	result.BucketURL = getEnvOrDie("CURRENCY_RATE_BUCKET_URL")
	result.DataFileObjectKey = getEnvOrDie("CURRENCY_RATE_DATA_FILE_PATH")

	return result
}

func getEnvOrDie(env string) string {
	if env == "" {
		panic("can not pass empty string as environment variable")
	}

	if v := os.Getenv(env); v != "" {
		return v
	}

	panic(env + " not defined as environment variable")
}

func getExchangeRateData(config *Config) ([]ExchangeRateRecord, error) {

	type row struct {
		Timestamp   time.Time `bigquery:"timestamp"`
		ExchagneBuy *big.Rat  `bigquery:"ex_buy"`
		Middle      *big.Rat  `bigquery:"middle"`
	}

	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, config.GoogleProjectID)
	if err != nil {
		return nil, err
	}

	query := fmt.Sprintf(`
	SELECT timestamp, MIN(ex_buy) as ex_buy, MIN(middle) as middle
	FROM`+" `%s.%s.%s` "+`
	GROUP BY timestamp
	ORDER BY timestamp ASC
	`, config.GoogleProjectID, config.BQDataset, config.BQTable)

	q := client.Query(query)
	it, err := q.Read(ctx)
	if err != nil {
		return nil, err
	}

	result := []ExchangeRateRecord{}

	for {
		var r row
		err := it.Next(&r)
		if err == iterator.Done {
			break
		}
		if err != nil {
			return nil, err
		}

		record := ExchangeRateRecord{Timestamp: r.Timestamp}
		record.ExchangeBuy, _ = r.ExchagneBuy.Float64()
		record.Middle, _ = r.Middle.Float64()

		result = append(result, record)
	}

	return result, nil
}

func updateRemoteFile(data ExchangeRateData, config *Config) error {
	ctx := context.Background()

	fmt.Printf("writing data to gcs: %s/%s\n", config.BucketURL, config.DataFileObjectKey)

	b, err := blob.OpenBucket(ctx, config.BucketURL)
	if err != nil {
		return fmt.Errorf("Failed to setup bucket: %s", err)
	}

	beforeWrite := func(as func(interface{}) bool) error {
		var sw *storage.Writer
		if as(&sw) {
			sw.PredefinedACL = "publicRead"
		}
		return nil
	}
	dataFileWriter, err := b.NewWriter(ctx, config.DataFileObjectKey, &blob.WriterOptions{
		ContentType: "application/javascript",
		BeforeWrite: beforeWrite,
	})
	defer dataFileWriter.Close()

	if err != nil {
		return err
	}

	_, err = dataFileWriter.Write([]byte("window.exchangeRate = "))
	if err != nil {
		return err
	}

	return json.NewEncoder(dataFileWriter).Encode(data)
}
