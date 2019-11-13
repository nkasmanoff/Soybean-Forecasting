dir_use = 'Documents/NYU/FALL2019/Courses/DS_GA_1001/Project/USDA_Data/'
setwd(dir_use)
folders = list.dirs(full.names = F)
folders = folders[2:length(folders)]

# This creates a list of dataframes, will loop through each directory of 
# datatype, and create a dataframe within the list component.
# If there are more than one file within the directory, it appends them to
# each other. Also, if there are columns filled with only NA values, it removes
# them since they are useless and confound the data downstream.
DF = list()
for (folder in folders) {
  DF[[folder]] = NULL
  for (file in list.files(folder)) {
    read_in = read.csv(paste(folder,file,sep = '/'),check.names = F,
                       stringsAsFactors = F)
    DF[[folder]] <- rbind(DF[[folder]],read_in)
  }
  orig = nrow(DF[[folder]])
  DF[[folder]] <- unique(DF[[folder]])
  new = nrow(DF[[folder]])
  print(ifelse(orig == new,'No duplicate values','duplicates removed'))
  
  columns_remove = c()
  for (col in colnames(DF[[folder]])) {
    if (sum(is.na(DF[[folder]][,col])) == nrow(DF[[folder]])) {
      columns_remove = c(columns_remove,col)
    }
  }
  DF[[folder]] <- DF[[folder]][,!(colnames(DF[[folder]]) %in% c(columns_remove,'COMMODITY'))]
}

repeated_cols_merged <- function(dataframe) {
  repeated_cols = c()
  for (col in colnames(dataframe)) {
    if (substr(col,nchar(col)-1,nchar(col)) %in% c('.x','.y')) {
      repeated_cols = c(repeated_cols,col)
    }
  }
  to_print = ifelse(length(repeated_cols) > 0,
                    cat('Following columns repeated (BAD)',c(repeated_cols)),
                    'No columns repeated (GOOD)')
  return(print(to_print))
}

repeated_cols <- function(dataframe1,dataframe2) {
  for (col in colnames(dataframe1)) {
    if (col %in% colnames(dataframe2)) {
      print(col)
    }
  }
}

# Data has ANSI codes to merge on, use that to merge data.

# Need to clean the data significantly, get rid of redundant columns so that the 
# merge outputs nicely.
repeated_cols(DF[[1]],DF[[2]])

DF_1_redundant_columns = c('REFERENCE PERIOD','PRODN PRACTICE')
DF_2_redundant_columns = c('ASD CODE','COUNTY ANSI')
DF[[1]] <- DF[[1]][,!(colnames(DF[[1]]) %in% DF_1_redundant_columns)]
DF[[2]] <- DF[[2]][,!(colnames(DF[[2]]) %in% DF_2_redundant_columns)]

colnames(DF[[1]])[colnames(DF[[1]]) == 'LOCATION'] <- 'REGION' 
colnames(DF[[2]])[colnames(DF[[2]]) == 'LOCATION'] <- 'STATE' 
colnames(DF[[3]])[colnames(DF[[3]]) == 'LOCATION'] <- 'STATE' 
colnames(DF[[4]])[colnames(DF[[4]]) == 'LOCATION'] <- 'STATE' 
colnames(DF[[5]])[colnames(DF[[5]]) == 'LOCATION'] <- 'STATE' 
colnames(DF[[6]])[colnames(DF[[6]]) == 'LOCATION'] <- 'STATE' 

DF_merge_test <- merge(DF[[1]],DF[[2]],by = c('YEAR','STATE ANSI'),all = T)

# will be an iterative process after merging each dataset, to check for
# repeated columns
repeated_cols_merged(DF_merge_test)

repeated_cols(DF_merge_test,DF[[3]])

DF_3_redundant_columns = c('STATE')
DF[[3]] <- DF[[3]][,!(colnames(DF[[3]]) %in% DF_3_redundant_columns)]
DF_merge_test <- merge(DF_merge_test,DF[[3]],
                       by = c('YEAR','STATE ANSI','REFERENCE PERIOD'),all = T)

repeated_cols_merged(DF_merge_test)
repeated_cols(DF_merge_test,DF[[4]])

DF_4_redundant_columns = c('STATE','REFERENCE PERIOD')
DF[[4]] <- DF[[4]][,!(colnames(DF[[4]]) %in% DF_4_redundant_columns)]
DF_merge_test <- merge(DF_merge_test,DF[[4]],
                       by = c('YEAR','STATE ANSI'),all = T)

# for now, I don't know how to merge Months with Reference Periods referring
# to weeks. I'm going to groupby month and average values for DF[[5]]

DF_5_grouped = NULL
for (State in unique(DF[[5]]$STATE)) {
  grouped_by_state <-  DF[[5]][DF[[5]]$STATE == State,]
  for (year in unique(grouped_by_state$YEAR)) {
    grouped_by_year <- grouped_by_state[grouped_by_state$YEAR == year,c('YEAR','STATE','STATE ANSI')][1,]
    to_add = grouped_by_state[grouped_by_state$YEAR == year,'ALL UTILIZATION PRACTICES in $ / BU']
    grouped_by_year$`ALL UTILIZATION PRACTICES in $ / BU` <- mean(to_add)
    DF_5_grouped <- rbind(DF_5_grouped,grouped_by_year)
  }
}

repeated_cols_merged(DF_merge_test)
repeated_cols(DF_merge_test,DF_5_grouped)

DF_5_redundant_columns = c('STATE')
DF_5_grouped <- DF_5_grouped[,!(colnames(DF_5_grouped) %in% DF_5_redundant_columns)]
DF_merge_test <- merge(DF_merge_test,DF_5_grouped,
                       by = c('YEAR','STATE ANSI'),all = T)

# Again, need to circle back to how to merge on the different form of 
# REFERENCE.PERIOD. For now I am grouping by mean, based off year/state
DF_6_grouped = NULL
for (State in unique(DF[[6]]$STATE)) {
  grouped_by_state <-  DF[[6]][DF[[6]]$STATE == State,]
  for (year in unique(grouped_by_state$YEAR)) {
    grouped_by_year <- grouped_by_state[grouped_by_state$YEAR == year,c('YEAR','STATE','STATE ANSI')][1,]
    to_add_col1 = as.numeric(grouped_by_state[grouped_by_state$YEAR == year,'ALL UTILIZATION PRACTICES in BU'])
    to_add_col2 = as.numeric(grouped_by_state[grouped_by_state$YEAR == year,'OFF FARM in BU'])
    to_add_col3 = as.numeric(grouped_by_state[grouped_by_state$YEAR == year,'ON FARM in BU'])
    grouped_by_year$`ALL UTILIZATION PRACTICES in BU` <- mean(to_add_col1)
    grouped_by_year$`OFF FARM in BU` <- mean(to_add_col2)
    grouped_by_year$`ON FARM in BU` <- mean(to_add_col3)
    DF_6_grouped <- rbind(DF_6_grouped,grouped_by_year)
  }
}


repeated_cols_merged(DF_merge_test)
repeated_cols(DF_merge_test,DF_6_grouped)

DF_6_redundant_columns = c('STATE')
DF_6_grouped <- DF_6_grouped[,!(colnames(DF_6_grouped) %in% DF_6_redundant_columns)]
DF_merge_test <- merge(DF_merge_test,DF_6_grouped,
                       by = c('YEAR','STATE ANSI'),all = T)

DF_merge_test$COMMODITY <- 'SOYBEAN'

colnames(DF_merge_test) <- unlist(lapply(colnames(DF_merge_test),function(x) gsub(' ','_',gsub(',','',x))))

DF_merge_test$COUNTY <- unlist(lapply(DF_merge_test$REGION,
                                      function(x) ifelse(!is.na(x),unlist(strsplit(x,','))[3],NA)))
DF_merge_test$REGION <- unlist(lapply(DF_merge_test$REGION,
                                      function(x) ifelse(!is.na(x),unlist(strsplit(x,','))[2],NA)))

# Reorder columns
DF_merge_test <- DF_merge_test[,c(56,11,4,57,2,5,6,1,3,27,7:10,12:26,28:55)]

# Check datatype of each column
unlist(lapply(colnames(DF_merge_test),
              function(x) paste(x,' : ',typeof(DF_merge_test[,x]))))

for (col in 11:54) {
  DF_merge_test[,col] <- as.numeric(gsub(',','',DF_merge_test[,col]))
}


write.table(DF_merge_test,sep = ',',quote = F,row.names = F,file = 'Merged_Data.csv')
