# Veggie-Tales


Team Name: Team Veggie Tales

Team Members: 
Peter Simone: ps4021
Rahul Zalkikar: rz1567
Rachana Swamy: rms816
Noah Kasmanoff: nsk367

Our goal is to forecast crop yield from different agricultural indicators, supported by research, by applying supervised machine learning models. We will not be using satellite images or mapping for this project, and instead leverage relevant qualitative and quantitative data from the United States Department of Agriculture (USDA) and the Federal Emergency Management Agency (FEMA). Predicting crop yield can help farmers and institutions increase crop production to meet the rapidly growing global demand for food. Given decreasing profit trends and current political policies (agricultural tariffs, etc.), a predictive crop yield model can increase profit margins for contemporary farmers by, for example, helping them reduce waste and increase production efficiency. This represents the value from a business perspective in being able to forecast supply necessary to support that crop yield. This would also help optimize the supply chains of farmers, or companies producing the crops, by allowing them to preemptively purchase more supply of certain crops if needed, essentially making their production more efficient and in turn improve profit margins.


To achieve this, we will work with datasets already provided by the USDA relating to agriculture. Our group will also be incorporating weather forecast using FEMA datasets. Specifically, we aim to develop our model based off of the following variables:  Crop type, region, datetime, adverse events, yield last 10 years, average yield, county,  yield across the entire crop type, yield across the entire region, precipitation, minimum air temperature (daily average), maximum air temperature (daily average), wind speed, relative humidity, proportion of land irrigated in the county, soil type. Our objective is to work with the features previously mentioned in order to predict the crop yield this upcoming time segment ,which will be a continuous variable. If we approach this as an ordinal classification problem (standardized degrees of increased/decreased crop yield across variable sets), then we might first at forecast a specific crop yield amount, we might attempt a baseline regression model and evaluate metrics such as RMSE. We will then expand these baseline models appropriately until we achieve a degree of actionable insights.

Data Sources and References:
https://quickstats.nass.usda.gov/
https://catalog.data.gov/dataset/disaster-declaration
https://iopscience.iop.org/article/10.1088/1748-9326/aae159
