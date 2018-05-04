mydata=read.csv(file=file.choose())
boxplot.stats(mydata$Alt)$out
plot(Alt~Time, mydata)
Time2 <- mydata$Time^2
Time3 <- mydata$Time^3
lfit = lm(mydata$Alt~mydata$Time + Time2 + Time3)
abline(lfit, col="red")
residual = resid(lfit)
boxplot.stats(residual)$out