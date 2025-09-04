library(tidyr)
library(ggplot2)
library(viridis)
bw <- theme_bw(base_size = 18) %+replace%
  theme(axis.text.x = element_text(
    angle = 45, hjust = 1, vjust = 1
  ))
theme_set(bw)
