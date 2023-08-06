Export CSV To Influx
====================

**Export CSV To Influx**: Process CSV data, and export the data to influx db

## Install

Use the pip to install the library. Then the binary **export_csv_to_influx** is ready.

```
pip install ExportCsvToInflux
```

## Features

1. **[Highlight :star2::tada::heart_eyes:]** Allow to use binary **export_csv_to_influx** to run exporter
2. **[Highlight :star2::tada::heart_eyes:]** Allow to check dozens of csv files in a folder
3. **[Highlight :star2::tada::heart_eyes::confetti_ball::four_leaf_clover::balloon:]** Auto convert csv data to int/float/string in Influx
4. **[Highlight :star2::tada::heart_eyes:]** Allow to match or filter the data by using string or regex.
5. **[Highlight :star2::tada::heart_eyes:]** Allow to count, and generate count measurement
6. Allow to limit string length in Influx
7. Allow to judge the csv has new data or not
8. Allow to use the latest file modify time as time column
9. Auto Create database if not exist
10. Allow to drop database before inserting data
11. Allow to drop measurements before inserting data

## Command Arguments

You could use `export_csv_to_influx -h` to see the help guide.

`-c, --csv`: Input CSV file path, or the folder path. `Mandatory`

`-db, --dbname`: InfluxDB Database name. `Mandatory`

`-m, --measurement`: Measurement name. `Mandatory`

`-fc, --field_columns`: List of csv columns to use as fields, separated by comma. `Mandatory`

`-d, --delimiter`: CSV delimiter. Default: ','. 

`-lt, --lineterminator`: CSV lineterminator. Default: '\n'. 

`-s, --server`: InfluxDB Server address. Default: localhost:8086.

`-u, --user`: InfluxDB User name. Default: admin

`-p, --password`: InfluxDB Password. Default: admin

`-t, --time_column`: Timestamp column name. Default column name: timestamp. 
    
If no timestamp column, the timestamp is set to the last file modify time for whole csv rows.
    
> Note: Also support the pure timestamp, like: 1517587275. Auto detected.
    
`-tf, --time_format`: Timestamp format. Default: '%Y-%m-%d %H:%M:%S' e.g.: 1970-01-01 00:00:00.

`-tz, --time_zone`: Timezone of supplied data. Default: UTC.

`-tc, --tag_columns`: List of csv columns to use as tags, separated by comma. Default: None

`-b, --batch_size`: Batch size when inserting data to influx. Default: 500.

`-lslc, --limit_string_length_columns`: Limit string length column, separated by comma. Default: None.

`-ls, --limit_length`: Limit length. Default: 20.

`-dd, --drop_database`: Drop database before inserting data. Default: False.

`-dm, --drop_measurement`: Drop measurement before inserting data. Default: False.

`-mc, --match_columns`: Match the data you want to get for certain columns, separated by comma. Match Rule: All matches, then match. Default: None.

`-mbs, --match_by_string`: Match by string, separated by comma. Default: None.

`-mbr, --match_by_regex`: Match by regex, separated by comma. Default: None.

`-fic, --filter_columns`: Filter the data you want to filter for certain columns, separated by comma. Filter Rule: Any one filter success, the filter. Default: None.

`-fibs, --filter_by_string`: Filter by string, separated by comma. Default: None.

`-fibr, --filter_by_regex`: Filter by regex, separated by comma. Default: None.

`-ecm, --enable_count_measurement`: Enable count measurement. Default: False.

`-fi, --force_insert_even_csv_no_update`: Force insert data to influx, even csv no update. Default: False.

`-fsc, --force_string_columns`: Force columns as string type, seperated as comma. Default: None

`-fintc, --force_int_columns`: Force columns as int type, seperated as comma. Default: None

`-ffc, --force_float_columns`: Force columns as float type, seperated as comma. Default: None


> **Note:** 
> 1. You could pass `*` to --field_columns to match all the fields: `--field_columns=*`, `--field_columns '*'`
> 2. CSV data won't insert into influx again if no update. Use to force insert: `--force_insert_even_csv_no_update=True`, `--force_insert_even_csv_no_update True`
> 3. If some csv cells have no value, auto fill the influx db based on column data type: `int: -999`, `float: -999.0`, `string: -`

## Programmatically

Also, we could run the exporter programmatically.

```
from ExportCsvToInflux import ExporterObject

exporter = ExporterObject()
exporter.export_csv_to_influx(...)

# You could get the export_csv_to_influx parameter details by:
print(exporter.export_csv_to_influx.__doc__)
```

## Sample

Here is the **demo.csv**.

``` 
timestamp,url,response_time
2019-07-11 02:04:05,https://jmeter.apache.org/,1.434
2019-07-11 02:04:06,https://jmeter.apache.org/,2.434
2019-07-11 02:04:07,https://jmeter.apache.org/,1.200
2019-07-11 02:04:08,https://jmeter.apache.org/,1.675
2019-07-11 02:04:09,https://jmeter.apache.org/,2.265
2019-07-11 02:04:10,https://sample-demo.org/,1.430
2019-07-12 08:54:13,https://sample-show.org/,1.300
2019-07-12 14:06:00,https://sample-7.org/,1.289
2019-07-12 18:45:34,https://sample-8.org/,2.876
```

1. Command to export whole data into influx:

    ``` 
    export_csv_to_influx \
    --csv demo.csv \
    --dbname demo \
    --measurement demo \
    --tag_columns url \
    --field_columns response_time \
    --user admin \
    --password admin \
    --force_insert_even_csv_no_update True \
    --server 127.0.0.1:8086
    ```

2. Command to export whole data into influx, **but: drop database**

    ```
    export_csv_to_influx \
    --csv demo.csv \
    --dbname demo \
    --measurement demo \
    --tag_columns url \
    --field_columns response_time \
    --user admin \
    --password admin \
    --server 127.0.0.1:8086 \
    --force_insert_even_csv_no_update True \
    --drop_database=True
    ```

3. Command to export part of data: **timestamp matches 2019-07-12 and url matches sample-\d+**

    ``` 
    export_csv_to_influx \
    --csv demo.csv \
    --dbname demo \
    --measurement demo \
    --tag_columns url \
    --field_columns response_time \
    --user admin \
    --password admin \
    --server 127.0.0.1:8086 \
    --drop_database=True \
    --force_insert_even_csv_no_update True \
    --match_columns=timestamp,url \
    --match_by_reg='2019-07-12,sample-\d+'
    ```
    
4. Filter part of data, and the export into influx: **url filter sample**

    ``` 
    export_csv_to_influx \
    --csv demo.csv \
    --dbname demo \
    --measurement demo \
    --tag_columns url \
    --field_columns response_time \
    --user admin \
    --password admin \
    --server 127.0.0.1:8086 \
    --drop_database True \
    --force_insert_even_csv_no_update True \
    --filter_columns timestamp,url \
    --filter_by_reg 'sample'
    ```

5. Enable count measurement. A new measurement named: **demo.count** generated, with match: **timestamp matches 2019-07-12 and url matches sample-\d+**

    ```
    export_csv_to_influx \
    --csv demo.csv \
    --dbname demo \
    --measurement demo \
    --tag_columns url \
    --field_columns response_time \
    --user admin \
    --password admin \
    --server 127.0.0.1:8086 \
    --drop_database True \
    --force_insert_even_csv_no_update True \
    --match_columns timestamp,url \
    --match_by_reg '2019-07-12,sample-\d+' \
    --enable_count_measurement True 
    ```
    
    The count measurement is:
    
    ```text
    select * from "demo.count"
 
    name: demo.count
    time                match_timestamp match_url total
    ----                --------------- --------- -----
    1562957134000000000 3               2         9
    ```

## Special Thanks

The lib is inspired by: [https://github.com/fabio-miranda/csv-to-influxdb](https://github.com/fabio-miranda/csv-to-influxdb)
