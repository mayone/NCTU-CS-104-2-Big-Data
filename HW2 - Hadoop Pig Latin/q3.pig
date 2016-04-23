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

DelayData = FOREACH Table GENERATE Year, Month, ArrDelay+DepDelay AS Delay;
YearMonth = GROUP DelayData BY (Year, Month);
MonthDelay = FOREACH YearMonth GENERATE FLATTEN(group) AS (Year, Month), AVG(DelayData.Delay) AS AvgDelay;
/*
MonthDelay = ORDER MonthDelay BY Year, AvgDelay;
DUMP MonthDelay;
*/

YearGroup = GROUP MonthDelay BY Year;
MinDelay = FOREACH YearGroup {
	MonthDelay = ORDER MonthDelay BY AvgDelay;
	MinDelay = LIMIT MonthDelay 1;
	GENERATE FLATTEN(MinDelay);
} 
DUMP MinDelay;
