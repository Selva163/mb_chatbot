CREATE OR REPLACE TABLE overall_data as 
            SELECT *,
            0 as is_forecasted
            FROM 'mb_chatbot/data/overall.csv';

INSERT into overall_data (well_name, metric_month, Total_Revenue, Net_Operating_Profit_to_WI_Owners,
Oil_Production_Tax, Oil_Sales_Bbls, Total_WI_Expenses, Workover_Cost, is_forecasted)

with last_4_months as (select well_name, metric_month, Total_Revenue, Net_Operating_Profit_to_WI_Owners,
Oil_Production_Tax, Oil_Sales_Bbls, Total_WI_Expenses, Workover_Cost
from oildata.main.overall_data
qualify row_number() over (partition by well_name order by metric_month desc) <5 
)

select well_name, '2025-01-01' as metric_month,
AVG(Total_Revenue) Total_Revenue
, AVG(Net_Operating_Profit_to_WI_Owners) Net_Operating_Profit_to_WI_Owners
, AVG(Oil_Production_Tax) Oil_Production_Tax
, AVG(Oil_Sales_Bbls) Oil_Sales_Bbls
, AVG(Total_WI_Expenses) Total_WI_Expenses
, 0 as Workover_Cost
, 1 as is_forecasted
from 
last_4_months
group by well_name;



INSERT into overall_data (well_name, metric_month, Total_Revenue, Net_Operating_Profit_to_WI_Owners,
Oil_Production_Tax, Oil_Sales_Bbls, Total_WI_Expenses, Workover_Cost, is_forecasted)

with last_4_months as (select well_name, metric_month, Total_Revenue, Net_Operating_Profit_to_WI_Owners,
Oil_Production_Tax, Oil_Sales_Bbls, Total_WI_Expenses, Workover_Cost
from oildata.main.overall_data
qualify row_number() over (partition by well_name order by metric_month desc) <5 
)

select well_name, '2025-02-01' as metric_month,
AVG(Total_Revenue) Total_Revenue
, AVG(Net_Operating_Profit_to_WI_Owners) Net_Operating_Profit_to_WI_Owners
, AVG(Oil_Production_Tax) Oil_Production_Tax
, AVG(Oil_Sales_Bbls) Oil_Sales_Bbls
, AVG(Total_WI_Expenses) Total_WI_Expenses
, 0 as Workover_Cost
, 1 as is_forecasted
from 
last_4_months
group by well_name;



INSERT into overall_data (well_name, metric_month, Total_Revenue, Net_Operating_Profit_to_WI_Owners,
Oil_Production_Tax, Oil_Sales_Bbls, Total_WI_Expenses, Workover_Cost, is_forecasted)

with last_4_months as (select well_name, metric_month, Total_Revenue, Net_Operating_Profit_to_WI_Owners,
Oil_Production_Tax, Oil_Sales_Bbls, Total_WI_Expenses, Workover_Cost
from oildata.main.overall_data
qualify row_number() over (partition by well_name order by metric_month desc) <5 
)

select well_name, '2025-03-01' as metric_month,
AVG(Total_Revenue) Total_Revenue
, AVG(Net_Operating_Profit_to_WI_Owners) Net_Operating_Profit_to_WI_Owners
, AVG(Oil_Production_Tax) Oil_Production_Tax
, AVG(Oil_Sales_Bbls) Oil_Sales_Bbls
, AVG(Total_WI_Expenses) Total_WI_Expenses
, 0 as Workover_Cost
, 1 as is_forecasted
from 
last_4_months
group by well_name;


INSERT into overall_data (well_name, metric_month, Total_Revenue, Net_Operating_Profit_to_WI_Owners,
Oil_Production_Tax, Oil_Sales_Bbls, Total_WI_Expenses, Workover_Cost, is_forecasted)

with last_4_months as (select well_name, metric_month, Total_Revenue, Net_Operating_Profit_to_WI_Owners,
Oil_Production_Tax, Oil_Sales_Bbls, Total_WI_Expenses, Workover_Cost
from oildata.main.overall_data
qualify row_number() over (partition by well_name order by metric_month desc) <5 
)

select well_name, '2025-04-01' as metric_month,
AVG(Total_Revenue) Total_Revenue
, AVG(Net_Operating_Profit_to_WI_Owners) Net_Operating_Profit_to_WI_Owners
, AVG(Oil_Production_Tax) Oil_Production_Tax
, AVG(Oil_Sales_Bbls) Oil_Sales_Bbls
, AVG(Total_WI_Expenses) Total_WI_Expenses
, 0 as Workover_Cost
, 1 as is_forecasted
from 
last_4_months
group by well_name;


INSERT into overall_data (well_name, metric_month, Total_Revenue, Net_Operating_Profit_to_WI_Owners,
Oil_Production_Tax, Oil_Sales_Bbls, Total_WI_Expenses, Workover_Cost, is_forecasted)

with last_4_months as (select well_name, metric_month, Total_Revenue, Net_Operating_Profit_to_WI_Owners,
Oil_Production_Tax, Oil_Sales_Bbls, Total_WI_Expenses, Workover_Cost
from oildata.main.overall_data
qualify row_number() over (partition by well_name order by metric_month desc) <5 
)

select well_name, '2025-05-01' as metric_month,
AVG(Total_Revenue) Total_Revenue
, AVG(Net_Operating_Profit_to_WI_Owners) Net_Operating_Profit_to_WI_Owners
, AVG(Oil_Production_Tax) Oil_Production_Tax
, AVG(Oil_Sales_Bbls) Oil_Sales_Bbls
, AVG(Total_WI_Expenses) Total_WI_Expenses
, 0 as Workover_Cost
, 1 as is_forecasted
from 
last_4_months
group by well_name;


INSERT into overall_data (well_name, metric_month, Total_Revenue, Net_Operating_Profit_to_WI_Owners,
Oil_Production_Tax, Oil_Sales_Bbls, Total_WI_Expenses, Workover_Cost, is_forecasted)

with last_4_months as (select well_name, metric_month, Total_Revenue, Net_Operating_Profit_to_WI_Owners,
Oil_Production_Tax, Oil_Sales_Bbls, Total_WI_Expenses, Workover_Cost
from oildata.main.overall_data
qualify row_number() over (partition by well_name order by metric_month desc) <5 
)

select well_name, '2025-06-01' as metric_month,
AVG(Total_Revenue) Total_Revenue
, AVG(Net_Operating_Profit_to_WI_Owners) Net_Operating_Profit_to_WI_Owners
, AVG(Oil_Production_Tax) Oil_Production_Tax
, AVG(Oil_Sales_Bbls) Oil_Sales_Bbls
, AVG(Total_WI_Expenses) Total_WI_Expenses
, 0 as Workover_Cost
, 1 as is_forecasted
from 
last_4_months
group by well_name;
