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

DelayData = FOREACH Table GENERATE Year, ArrDelay+DepDelay AS Delay;
SplitYear = GROUP DelayData BY Year;

AvgDelay = FOREACH SplitYear GENERATE group AS Year, AVG(DelayData.Delay);
AvgDelay = ORDER AvgDelay BY Year;
DUMP AvgDelay;

MaxDelay = FOREACH SplitYear GENERATE group AS Year, MAX(DelayData.Delay);
MaxDelay = ORDER MaxDelay BY Year;
DUMP MaxDelay;
