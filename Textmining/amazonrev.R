#For Text Mining assignment
#1) Extract reviews of any product from ecommerce website like amazon
#2) Perform emotion minin

library(rvest)
library(XML)
library(magrittr)

# Amazon Reviews Acer nitro 5 gaming laptop #############################
aurl <- "https://www.amazon.in/Acer-15-6-inch-Graphics-Obsidian-AN515-55/product-reviews/B088FLY29Z/ref=cm_cr_getr_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
amazon_reviews1 <- NULL
#Only review page limit is upto 18 so maximum page limit is set to 18
for (i in 1:18){
  murl <- read_html(as.character(paste(aurl,i,sep="")))
  rev <- murl %>%  ##<-sequential execution in pipeline
    html_nodes(".review-text") %>%
    html_text()
  amazon_reviews1 <- c(amazon_reviews1,rev)
}

#Storing into TextFile
write.table(amazon_reviews1,"filepath/Acernitro5.txt",row.names=FALSE)

x = readLines(file.choose()) 	# first, read-in data from "amazon acer nitro 5 reviews.txt"

library(tm)
library(slam)
library(topicmodels)


length(x)			# check its length
x1 = Corpus(VectorSource(x))  	# Constructs a source for a vector as input
x1
#View(x1)
x1 = tm_map(x1, stripWhitespace) 	# removes white space
x1 = tm_map(x1, tolower)		# converts to lower case
x1 = tm_map(x1, removePunctuation)	# removes punctuation marks
x1 = tm_map(x1, removeNumbers)		# removes numbers in the documents
x1 = tm_map(x1, removeWords, c(stopwords('english'), "project", "null"))
#x1 = tm_map(x1, PlainTextDocument)

# build a term-document matrix
mydata.dtm3 <- TermDocumentMatrix(x1)
mydata.dtm3

dim(mydata.dtm3)
dtm <-as.DocumentTermMatrix(mydata.dtm3)

rowTotals <- apply(dtm , 1, sum)

dtm.new   <- dtm[rowTotals> 0, ]


library(NLP)
lda <- LDA(dtm.new, 10) # find 10 topics
term <- terms(lda, 5) # first 5 terms of every topic
term

tops <- terms(lda)
tb <- table(names(tops), unlist(tops))
tb <- as.data.frame.matrix(tb)

cls <- hclust(dist(tb), method = 'ward.D2')
par(family = "HiraKakuProN-W3")
plot(cls)

####################### Emotion mining ##############################
library("syuzhet")

my_example_text <- readLines("filepath/Acernitro5.txt")
s_v <- get_sentences(my_example_text)
class(s_v)
str(s_v)
head(s_v)


sentiment_vector <- get_sentiment(s_v, method = "bing")
head(sentiment_vector)

afinn_s_v <- get_sentiment(s_v, method = "afinn")
head(afinn_s_v)

nrc_vector <- get_sentiment(s_v, method="nrc")
head(nrc_vector)


###Using bing method vector for mining
sum(sentiment_vector)
mean(sentiment_vector)

summary(sentiment_vector)

# plot
plot(sentiment_vector, type = "l", main = "Plot Trajectory",
     xlab = "Narrative Time", ylab = "Emotional Valence")
abline(h = 0, col = "red")

# To extract the sentence with the most negative emotional valence
negative <- s_v[which.min(sentiment_vector)]
negative

# more depth
poa_v<-my_example_text

poa_sent <- get_sentiment(poa_v, method="bing")
plot(
  poa_sent, 
  type="h", 
  main="Example Plot Trajectory", 
  xlab = "Narrative Time", 
  ylab= "Emotional Valence"
)


# categorize each sentence by eight emotions
nrc_data <- get_nrc_sentiment(s_v)

# subset

sad_items <- which(nrc_data$sadness > 0)
head(s_v[sad_items])

# To view the emotions as a barplot
barplot(sort(colSums(prop.table(nrc_data[, 1:8]))), horiz = T, cex.names = 0.7,
        las = 1, main = "Emotions", xlab = "Percentage",
        col = 1:8)
