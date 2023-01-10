package main

import (
	"net/http"
	"github.com/gin-gonic/gin"
    "encoding/json"
    "os"
	"fmt"
	"io/ioutil"
)

type Config struct {
    Port string
}

func main() {

	confFile, err := os.Open("conf.json")
	if err != nil {
		panic(err)
	}
	
	defer confFile.Close()
    rawFile, err := ioutil.ReadAll(confFile)
    if err != nil {
      panic(err)
    }
	applicationConfig := Config{}
    err = json.Unmarshal(rawFile, &applicationConfig)
	if err != nil {
		panic(err)
	}

	fmt.Printf("%+v",applicationConfig)

	listener_port := ":" + applicationConfig.Port
	r := gin.Default()
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "Health/OK",
		})
	})

	r.Run(listener_port)
}
