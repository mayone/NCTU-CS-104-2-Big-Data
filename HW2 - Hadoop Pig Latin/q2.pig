Table = LOAD '$input' USING PigStorage(',') AS (
    Year:chararray,
    Month:chararray,
    DayofMonth:chararray,
    DayOfWeek:chararray,
    DepTime:chararray,
    CRSDepTime:chararray,
    ArrTime:chararray,
    CRSArrTime:chararray,
    UniqueCarrier:chararray,
    FlightNum:chararray,
    TailNum:chararray,
    ActualElapsedTime:chararray,
    CRSElapsedTime:chararray,
    AirTime:chararray,
    ArrDelay:int,
    DepDelay:int,
    Origin:chararray,
    Dest:chararray,
    Distance:chararray,
    TaxiIn:chararray,
    TaxiOut:chararray,
    Cancelled:chararray,
    CancellationCode:chararray,
    Diverted:chararray,
    CarrierDelay:chararray,
    WeatherDelay:chararray,
    NASDelay:chararray,
    SecurityDelay:chararray,
    LateAircraftDelay:chararray);

Table = FILTER Table BY Year != 'Year';

DelayData = FOREACH Table GENERATE Year, WeatherDelay;
DelayData = FILTER DelayData BY WeatherDelay != '0' AND WeatherDelay != 'NA';
DelayData = FOREACH DelayData GENERATE Year, (int)WeatherDelay;

DelayGroup = GROUP DelayData ALL;
DelayCount = FOREACH DelayGroup GENERATE COUNT(DelayData);
DUMP DelayCount

AvgDelay = FOREACH DelayGroup GENERATE AVG(DelayData.WeatherDelay);
DUMP AvgDelay;
