package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strings"
)

func main() {
	bs, err := ioutil.ReadAll(os.Stdin)
	if err != nil {
		log.Fatal(err)
	}

	i := 0

	b := new(strings.Builder)
	fmt.Fprintf(b, "const part%d = [", i)
	fmt.Fprint(b, bs[0])
	for _, c := range bs[1:] {
		if len(b.String()) >= 990000 {
			fmt.Fprintf(b, "];")

			filepath := new(strings.Builder)
			fmt.Fprintf(filepath, "/Users/ascholtz/mydata/udf-wasm-bigquery/out/part%d.js", i)
			
	    	ioutil.WriteFile(filepath.String(), []byte(b.String()), 0644)
    		i = i + 1
    		b = new(strings.Builder)
			fmt.Fprintf(b, "const part%d = [", i)
			fmt.Fprint(b, c)
    	} else {
    		fmt.Fprintf(b, ",%d", c)
    	}
	}

	fmt.Fprintf(b, "];")
	filepath := new(strings.Builder)
	fmt.Fprintf(filepath, "/Users/ascholtz/mydata/udf-wasm-bigquery/out/part%d.js", i)
	ioutil.WriteFile(filepath.String(), []byte(b.String()), 0644)
}