package main

import (
	"log"
	"runtime"
	"time"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/cloudwatch"
)

func main() {
	publishMemoryToCloudWatch()
}

func publishMemoryToCloudWatch() {
	// create service client
	mySession := session.Must(session.NewSession())
	cfg := aws.NewConfig().WithRegion("us-east-1")
	svc := cloudwatch.New(mySession, cfg)

	// get memory statistics
	var m runtime.MemStats
	runtime.ReadMemStats(&m)
	allocMB := m.Alloc / 1024 / 1024

	// publish memory statistics
	log.Println("Sending metric of", allocMB, "MB Alloc at", time.Now().Format("15:04:05"))
	_, err := svc.PutMetricData(&cloudwatch.PutMetricDataInput{
		Namespace: aws.String("my_custom_metrics"),
		MetricData: []*cloudwatch.MetricDatum{
			&cloudwatch.MetricDatum{
				MetricName: aws.String("Memory_Alloc"),
				Unit:       aws.String("Megabytes"),
				Value:      aws.Float64(float64(allocMB)),
			},
		},
	})

	// log on error, eg. Permission Denied - missing cloudwatch:PutMetricData in EC2 Instance Profile (the assigned IAM Role)
	if err != nil {
		log.Println("Error adding metrics:", err.Error())
	}
}
