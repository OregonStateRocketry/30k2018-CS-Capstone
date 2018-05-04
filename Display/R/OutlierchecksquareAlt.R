mydata=read.csv(file=file.choose())
boxplot.stats(mydata$Alt)$out
plot(Alt~Time, mydata)
Time2 <- mydata$Time^2
lfit = lm(mydata$Alt~mydata$Time + Time2)
abline(lfit, col="red")
residual = resid(lfit)
boxplot.stats(residual)$out