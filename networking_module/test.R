save.image('test.RData')

library(dplyr)
library(jsonlite)

membernames<-flatten(fromJSON(file('riha_sample.json'))) %>% distinct(member_code, member_name)
dat<-readRDS("dat.rds")

dat.membercodes<-union(unique(dat$clientmembercode), unique(dat$servicemembercode))
length(dat.membercodes)

length(unique(membernames$member_code))

dat.membercodes %in% unique(membernames$member_code)

data.frame(
  dat.membercodes=dat.membercodes,
  present.in.riha=dat.membercodes %in% unique(membernames$member_code)
) %>% filter(present.in.riha==F)

membernames %>% filter(member_code %in% {membernames %>% count(member_code) %>% filter(n>1) %>% .$member_code})

membernames %>% filter(member_name %in% {membernames %>% count(member_name) %>% filter(n>1) %>% .$member_name}) %>% select(member_name, member_code) %>% arrange(member_name)
