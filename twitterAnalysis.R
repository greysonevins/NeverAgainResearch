```r
options(scipen=10)

fun_check_packages <- function(x){
  for (i in seq(1,length(x))){
    if (!x[i] %in% installed.packages()){
    install.packages(x[i])}
    library(x[i],character.only=TRUE)}
}
packs = c('ggplot2','gridExtra', 'dplyr','tidyr', 'knitr', 'devtools', 'zoo', 'cowplot')
fun_check_packages(packs); rm(packs, fun_check_packages)

library(oii)
l

tweets15 = read.csv("data/tweets15Days.csv")
tweets30 = read.csv("data/tweets30Days.csv")
tweets60 = read.csv("data/tweets60Days.csv")

lengthData = read.csv("data/lengthOfTweets.csv")
tweetsPolitical = read.csv("data/politicsOfTweets.csv")
tweet15Ave = aggregate(tweets15$Tweets, by=list(tweets15$Times), FUN=mean);
tweet30Ave = aggregate(tweets30$Tweets, by=list(tweets30$Times), FUN=mean);
tweet60Ave = aggregate(tweets60$Tweets, by=list(tweets60$Times), FUN=mean);
tweets60[[3]] <- as.POSIXlt(tweets60[[3]])
tweets30[[3]] <- as.POSIXlt(tweets30[[3]])
tweets15[[3]] <- as.POSIXlt(tweets15[[3]])
tweet15Ave[[1]] <- as.POSIXlt(tweet15Ave[[1]])
tweet30Ave[[1]] <- as.POSIXlt(tweet30Ave[[1]])
tweet60Ave[[1]] <- as.POSIXlt(tweet60Ave[[1]])


ggplot() +
  geom_line(data = tweets15,  aes(x = Times, y = Tweets, group = Location, colour = Location)) +
  xlab('Times') +
  ggtitle('Tweets over 4 days 15 Mins') +
  scale_x_datetime(date_breaks = "12 hour") +
  theme(axis.text.x = element_text(angle = 25, vjust = 1.0, hjust = 1.0))+
  geom_line(data = tweet15Ave, aes(x=Group.1, y=x),
            color = 'black', size = 0.75)

ggplot() +
  geom_line(data = tweets30,  aes(x = Times, y = Tweets, group = Location, colour = Location)) +
  xlab('Times') +
  ggtitle('Tweets over 4 days 30 Mins') +
  scale_x_datetime(date_breaks = "12 hour") +
  theme(axis.text.x = element_text(angle = 25, vjust = 1.0, hjust = 1.0))+
  geom_line(data = tweet30Ave, aes(x=Group.1, y=x),
            color = 'black', size = 0.75)

ggplot() +
  geom_line(data = tweets60,  aes(x = Times, y = Tweets, group = Location, colour = Location)) +
  xlab('Times') +
  ggtitle('Tweets over 4 days 60 Mins') +
  scale_x_datetime(date_breaks = "12 hour") +
  theme(axis.text.x = element_text(angle = 25, vjust = 1.0, hjust = 1.0))+
  geom_line(data = tweet60Ave, aes(x=Group.1, y=x),
            color = 'black', size = 0.75)

trumpTweets <- tweetsPolitical$tweetsPerTrumpVote
clintonTweets <- tweetsPolitical$tweetsPerHillaryVote

oii.summary(trumpTweets)
oii.summary(clintonTweets)
ggplot(tweetsPolitical, aes(x= votingRecord, y=tweetsPerTrumpVote, colour="green", label=X))+
  geom_point(colour=ifelse(tweetsPolitical$votingRecord>0.0,"blue", "red")) +geom_text(aes(label=ifelse(tweetsPerTrumpVote>1144 & votingRecord<0.0,as.character(X),'')),hjust=0, vjust=0)

Trump <- subset(tweetsPolitical, votingRecord < 0.0)
Clinton <- subset(tweetsPolitical, votingRecord > 0.0)
oii.summary(Trump$tweetsPerHillaryVote)
oii.summary(Trump$tweetsPerTrumpVote)

oii.summary(Clinton$tweetsPerHillaryVote)
oii.summary(Clinton$tweetsPerTrumpVote)

ggplot(tweetsPolitical, aes(x= votingRecord, y=tweetsPerHillaryVote, colour="red and blue", label=X))+
  geom_point(colour=ifelse(tweetsPoltical$votingRecord>0.0,"blue", "red")) +geom_text(aes(label=ifelse(tweetsPerHillaryVote<1792 & votingRecord>0.00,as.character(X),'')),hjust=0, vjust=0)

Trump <- subset(tweetsPolitical,votingRecord < 0.0)
Clinton <- subset(tweetsPolitical, votingRecord > 0.0)
oii.summary(Trump$totals)
#trump 3920 >>Texas is close but not there

#5,567
oii.summary(Clinton$totals)

##NonNormalized

ggplot(tweetsPolitical, aes(x= votingRecord, y=totals, colour="red and blue", label=X))+
  geom_point(colour=ifelse(tweetsPolitical$votingRecord>0.0,"blue", "red")) +geom_text(aes(label=ifelse(totals>5567 & votingRecord>0.00 | totals>3920 & votingRecord<0.00,as.character(X),'')),hjust=0, vjust=0)

#Normalized by Voting Record
Trump <- subset(tweetsPolitical,votingRecord < 0.0)
Clinton <- subset(tweetsPolitical, votingRecord > 0.0)
oii.summary(Trump$totalsNorm)
#trump 318

#546
oii.summary(Clinton$totalsNorm)

ggplot(tweetsPolitical, aes(x= votingRecord, y=totalsNorm, colour="red and blue", label=X))+
  geom_point(colour=ifelse(tweetsPolitical$votingRecord>0.0,"blue", "red")) +geom_text(aes(label=ifelse(totalsNorm>543 & votingRecord>0.00 | totalsNorm>318 & votingRecord<0.00,as.character(X),'')),hjust=0, vjust=0)


TrumpLength <- subset(lengthData, politicsN <0.0 )
ClintonLength <- subset(lengthData, politicsN >0.0 )
oii.summary(TrumpLength$textLength)
#roughly the same
oii.summary(ClintonLength$textLength)

##Engagement by tweet Length seems pointless

lengthFLoridaControl <- subset(lengthData, location != "Florida" )

hist(ClintonLength$textLength)
hist(TrumpLength$textLength)
hist(lengthData$textLength)
oii.summary(lengthFLoridaControl$textLength)
#18  -2SD 6 +2SD 30

LowerSD <- subset(lengthFLoridaControl, textLength < 6.0)
UpperSD <- subset(lengthFLoridaControl, textLength >30)

oii.freq(LowerSD$location)
oii.freq(UpperSD$location)

controlFlorida <- subset(tweetsPolitical, X!= "Florida")
TrumpNorm <- subset(controlFlorida,votingRecord < 0.0)
ClintonNorm <- subset(controlFlorida, votingRecord > 0.0)
oii.summary(TrumpNorm$totalsNorm)
#trump 270

#546
oii.summary(ClintonNorm$totalsNorm)
Trump <- subset(controlFlorida,votingRecord < 0.0)
Clinton <- subset(controlFlorida, votingRecord > 0.0)
oii.summary(Trump$totals)
#trump 2500

#5569
oii.summary(Clinton$totals)

ggplot(controlFlorida, aes(x= votingRecord, y=totals, colour="red and blue", label=X))+
  geom_point(colour=ifelse(controlFlorida$votingRecord>0.0,"blue", "red")) +geom_text(aes(label=ifelse(totals>5569 & votingRecord>0.00 | totals>2500 & votingRecord<0.00,as.character(X),'')),hjust=0, vjust=0)

ggplot(controlFlorida, aes(x= votingRecord, y=totalsNorm, colour="red and blue", label=X))+
  geom_point(colour=ifelse(controlFlorida$votingRecord>0.0,"blue", "red")) +geom_text(aes(label=ifelse(totalsNorm>546  & votingRecord>0.00 | totalsNorm>270 & votingRecord<0.00,as.character(X),'')),hjust=0, vjust=0)

oii.summary(controlFlorida$totals)
oii.summary(controlFlorida$totalsNorm)
# 1122 +2SD 4048 no -2SD

ggplot(controlFlorida, aes(x= votingRecord, y=totals, colour="red and blue", label=X))+
  geom_point(colour=ifelse(controlFlorida$votingRecord>0.0,"blue", "red")) +geom_text(aes(label=ifelse(totals>4048 ,as.character(X),'')),hjust=0, vjust=0)

ggplot(controlFlorida, aes(x= votingRecord, y=totalsNorm, colour="red and blue", label=X))+
  geom_point(colour=ifelse(controlFlorida$votingRecord>0.0,"blue", "red")) +geom_text(aes(label=ifelse(totalsNorm>543 & votingRecord>0.00 | totalsNorm>270 & votingRecord<0.00,as.character(X),'')),hjust=0, vjust=0)+
 geom_smooth(color = 'green', method = 'lm', se = F) +
 annotate('text', label = 'Green R-squared = 0.4204', x=-0.08, y=540) +
 annotate('text', label = 'Black R-squared = 0.0099*', x=0.03, y=420) +
 annotate('text', label = 'Purple R-squared = 0.3959', x=-0.15, y=340) +
 geom_smooth(data=Clinton, aes(x=votingRecord, y=totalsNorm),color = 'black', method = 'lm', se = FALSE) +
 geom_smooth(data=Trump, aes(x=votingRecord, y=totalsNorm),color = 'purple', method = 'lm', se = FALSE)




summary(lm(totalsNorm ~ votingRecord, data=controlFlorida))
#0.4204
summary(lm(totals ~ votingRecord, data=controlFlorida))
#0.2064
summary(lm(totalsNorm ~ votingRecord, data=tweetsPolitical))
#0.3982
summary(lm(totals ~ votingRecord, data=tweetsPolitical))
#0.1633

summary(lm(totalsNorm ~ votingRecord, data=Clinton))
#0.009895R
#225.49
summary(lm(totalsNorm ~ votingRecord, data=Trump))
#0.3959
#464

ggplot(lengthData, aes(politicsN, textLength)) +
  geom_point(color =ifelse(lengthData$politicsN>0.0, "blue", "red"), size = 0.1) +
  labs(x = 'Political Leaning', y= 'Number of Words in Tweet') +
  ggtitle('Political Alligance vs. Length of Tweet')
ggsave("twLengthByVote.png")



#224  442 no -2SD


my_ecdf <- ecdf(lengthData$textLength)

df.ecdf <- data.frame(x = sort(lengthData$textLength),
                y = my_ecdf(sort(lengthData$textLength) ))
ggplot(data = df.ecdf, aes(x, y) ) +
  geom_line() +
  geom_point(color="blue") +
  ggtitle('ECDF of # of Words Used') +
  xlab('Length of Tweet in Words') +
  ylab('Cumulative probability')

ggsave("ecdfWords.png")

```
