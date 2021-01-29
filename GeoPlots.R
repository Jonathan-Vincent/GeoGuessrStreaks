require(ggplot2)
library(scales)

GeoPlotData = GeoData


America = c('Mexico','Guatemala','Costa Rica','Dominican Republic',
          'Ecuador','Chile','Uruguay','Argentina','Colombia','Peru','Brazil',
          'United States','Canada')

Europe = c('France','Spain','Portugal','Belgium','Luxembourg','Germany','Netherlands',
             'Switzerland','Italy','Austria','Slovenia','Denmark','Norway','Sweden',
             'Finland','Czech Republic','Slovakia','Hungary','Poland','Lithuania',
             'Latvia','Estonia','Croatia','Serbia','North Macedonia','Albania',
             'Greece','Bulgaria','Turkey','Romania','Ukraine','Russia','United Kingdom',
           'Ireland','Malta','Montenegro','Iceland')

Africa = c('Egypt','Tunisia','Senegal','Ghana','Kenya','Nigeria','Uganda',
             'South Africa','Lesotho','Eswatini','Botswana')


GeoPlotData$Region = 'Asia and Oceania'
GeoPlotData[GeoPlotData$country %in% America,]$Region = 'The Americas'
GeoPlotData[GeoPlotData$country %in% Europe,]$Region = 'Europe'
GeoPlotData[GeoPlotData$country %in% Africa,]$Region = 'Africa'

breaks = append(10*0:10,c(110,120))


ticklabels = c('0','10','20','30','40','50','60','70','80','90','100','Locations','Attempts')

p<-ggplot(data=GeoPlotData, aes(y=reorder(country, srate), x=100*srate,fill=Region)) +
  geom_bar(stat="identity")+
  theme_minimal()+
  ylab(element_blank())+
  xlab('Success Rate (%)')+
  geom_text(aes(label=paste(sprintf("%.01f", srate*100), "%")), size=2.5,hjust=-0.1) +
  geom_text(aes(x=110,label=locations), size=2.5) +
  geom_text(aes(x=120,label=attempts), size=2.5) +
  geom_text(aes(x=127,label=country), size=3,hjust=0,alpha=0.8) +
  scale_fill_brewer(palette = "Set2")+
  scale_x_continuous(limits=c(0,150),expand=c(0,0),breaks=breaks,labels = ticklabels,sec.axis = sec_axis(~ . * 1,breaks=breaks,labels = ticklabels))+
  labs(title = 'GeoGuessr - Accuracy of Guesses by Country',
       subtitle = '42,642 guess attempts by 538 players in the Country Streak Gamemode\nTaken from December Streak Stacker 1-9 and January Streak Stacker 1-4 on Reddit')+
  theme(plot.title = element_text(face = 'bold',size=12),
        plot.subtitle = element_text(size=9),
        legend.title = element_blank(),
        legend.position='bottom',
        legend.spacing.x = unit(0.3, 'cm'),
        panel.grid.minor=element_blank(),
        panel.grid.major = element_blank())


