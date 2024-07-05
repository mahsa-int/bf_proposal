import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass
import plotly.express as px
from typing import List
import numpy as np
from scipy.stats import gaussian_kde
import seaborn as sns
from utils.transform_data import hour_bins
import missingno as msno
import math

@pd.api.extensions.register_dataframe_accessor("api_bfood")
@dataclass
class APIPandas:
    data: pd.DataFrame
    metrics = ['median', 'mean', 'sum', 'std', 'var', 'skew', 'kurt', 'count']
    common_na_strings = ("missing","NA","N A","N/A","na","NULL","null","","?","*",".","(none)","(not set)")
    colors = ['#54c7ec', '#26c29f', '#2ecc71', '#f1c40f', '#e67e22','#e74c3c', '#9b59b6', '#3498db', '#2980b9', '#16a085']

    def __post_init__(self):
        #Hour Categorization
        self.data['HourBins'] = self.data['hour'].apply(hour_bins)
        #Nulls Imputation
        self.data['Source'] = self.data['Source'].replace(to_replace=self.common_na_strings,value=np.nan)
        #Tranform Objects into Categories
        categories = {
            'Browser': 'category',
            'Channel': 'category',
            'OS': 'category',
            'DeviceType': 'category',
            'Source': 'category',
            'HourBins': 'category'
        }
        self.data = self.data.astype(categories)
    
    def null_chart(self):
        fig, axes = plt.subplots(1,2,figsize=(12,6))
        fig.text(0.5, 0, 'Fig 0.1 MNAR indica que los valores nulos no están distribuidos aleatoriamente.', ha='center')
        msno.matrix(self.data,ax=axes[0], sparkline=False)
        msno.matrix(self.data.sort_values(by=['Channel'],ascending=False),ax=axes[1], sparkline=False)
        axes[0].set_title('Sorted Randomly', fontdict={'fontsize': 12, 'fontweight': 'bold'})
        axes[1].set_title('Sorted By Channel', fontdict={'fontsize': 12, 'fontweight': 'bold'})
        axes[0].tick_params(axis='both', which='major', labelsize=10)
        axes[1].tick_params(axis='both', which='major', labelsize=10)
        plt.suptitle('Missing not At Random (MNAR)',fontweight='bold')
        plt.tight_layout()
        return fig

    def weekend_weekday_rate(self, cat_col, num_col):
        weekend_channel_visits = self.data.groupby(cat_col, observed=False)[num_col].sum()
        channel_visits = self.data.groupby(cat_col, observed=False)['UserId'].count()

        weekend_channel_prop = weekend_channel_visits / channel_visits
        channel_dist = self.data[cat_col].value_counts(normalize=True)
        channel_dist_dict = {channel: f"{proportion * 100:.2f}%" for channel, proportion in channel_dist.items()}

        n_categories = len(weekend_channel_prop)
        nrows = math.ceil(n_categories / 3) 
        ncols = min(n_categories, 3)

        fig, axes = plt.subplots(nrows, ncols, figsize=(15, 5 * nrows))
        if nrows == 1 and ncols == 1:
            axes = [axes]
        else:
            axes = axes.flatten()

        colors = ['#54c7ec', '#26c29f']

        for i, (channel, wkn_prop) in enumerate(weekend_channel_prop.sort_values(ascending=False).items()):
            if i < len(axes):
                wday_prop = 1 - wkn_prop
                labels = ['Weekend', 'Weekday']
                sizes = [wkn_prop, wday_prop]
                axes[i].pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
                axes[i].set_title(f'{channel.capitalize()}\n{channel_dist_dict.get(channel, "N/A")} Users', fontdict={'fontsize': 12, 'fontweight': 'bold'})

        # Eliminar ejes sobrantes
        for i in range(n_categories, len(axes)):
            fig.delaxes(axes[i])

        plt.suptitle('%Visits Weekends & Weekdays', fontweight='bold', fontsize=16)
        plt.tight_layout()
        
        # Ajustar la leyenda fuera de los subplots
        fig.legend(labels, loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=2)
        
        # Ajustar el espacio entre subplots
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15, wspace=0.3, hspace=0.4)
        
        return fig


    def barplot(self,yaxis,xaxis,metric,aggr):

        options = {
                    # 'median':self.data.groupby([yaxis,xaxis], observed=False)[metric].median().reset_index(),
                    # 'mean':self.data.groupby([yaxis,xaxis], observed=False)[metric].mean().reset_index(),
                    'sum':self.data.groupby([yaxis,xaxis], observed=False)[metric].sum().reset_index(),
                    # 'std':self.data.groupby([yaxis,xaxis], observed=False)[metric].std().reset_index(),
                    # 'var':self.data.groupby([yaxis,xaxis], observed=False)[metric].var().reset_index(),
                    # 'skew':self.data.groupby([yaxis,xaxis], observed=False)[metric].skew().reset_index(),
                    'count': self.data.groupby([yaxis,xaxis], observed=False)[metric].count().reset_index()
                    }

        top_down = list(self.data[f'{yaxis}'].value_counts().sort_values(ascending=False).index)
        data = options[aggr]
        data[f'%{metric} By {yaxis}'] = (data[metric] / data.groupby(yaxis, observed=False)[metric].transform('sum') * 100).round(2)
        colors = self.colors
        device_types = data[xaxis].unique()
        color_map = {device_type: colors[i % len(colors)] for i, device_type in enumerate(device_types)}

        fig = px.bar(
            data,
            x=f'{yaxis}',
            y=f'%{metric} By {yaxis}',
            color=f'{xaxis}',
            text=f'%{metric} By {yaxis}',
            title=f'Top-Down Dist. {metric} by {yaxis} and {xaxis}',
            labels={f'%{metric} By {yaxis}':'Percentage'},
            hover_data={f'{metric}':True},
            height=500,
            template='plotly_white',
            color_discrete_map=color_map,
            category_orders={f'{yaxis}': top_down})

        fig.update_yaxes(range=[0, 100])
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='inside')

        return fig
        
    def metrics_viewer(self,indexa,indexb,aggr,metric):
        options = {
                    'median':self.data.groupby([indexa,indexb],observed=False)[aggr].median().reset_index(),
                    'mean':self.data.groupby([indexa,indexb],observed=False)[aggr].mean().reset_index(),
                    'sum':self.data.groupby([indexa,indexb],observed=False)[aggr].sum().reset_index(),
                    'std':self.data.groupby([indexa,indexb],observed=False)[aggr].std().reset_index(),
                    'var':self.data.groupby([indexa,indexb],observed=False)[aggr].var().reset_index(),
                    'skew':self.data.groupby([indexa,indexb],observed=False)[aggr].skew().reset_index(),
                    'count': self.data.groupby([indexa, indexb],observed=False)[aggr].count().reset_index()
                    }

        data = options[metric]
        data[f'%{metric.capitalize()} By {indexb}'] = (data[aggr] / data.groupby(indexb, observed=False)[aggr].transform('sum') * 100).map('{:.2f}%'.format)
        data[f'%{metric.capitalize()} By {indexa}'] = (data[aggr] / data.groupby(indexa, observed=False)[aggr].transform('sum') * 100).map('{:.2f}%'.format)
        data.set_index([indexa,indexb],inplace=True)
        return data


    def hourkde_overall(self,feature):
        
        fig, axes = plt.subplots(1, 1, figsize=(15, 6))
        sns.histplot(data=self.data,x='hour',hue=feature,stat='probability',multiple='stack',kde=True,ax=axes)

        kde = gaussian_kde(self.data['hour'], bw_method='scott')
        x_vals = np.linspace(self.data['hour'].min(), self.data['hour'].max(), 1000)
        y_vals = kde(x_vals)

        max_prob_hour = x_vals[np.argmax(y_vals)]

        plt.axvline(max_prob_hour, color='red', linestyle='--')
        plt.annotate(f'Max prob: {max_prob_hour:.2f}', xy=(max_prob_hour, max(y_vals)),
                    xytext=(max_prob_hour + 0.005, max(y_vals) + 0.005))

        plt.title(f'{feature} Overall')

        return fig


    def single_hourkde(self,feature):
        channels = self.data[feature].value_counts(normalize=True).sort_values(ascending=False)*100
        num_channels = len(channels)

        fig, axes = plt.subplots(3, ncols=int(np.ceil(num_channels / 3)), figsize=(15, 10))
        axes = axes.flatten()

        for idx, (channel,value) in enumerate(channels.items()):
            ax = axes[idx]
            data = self.data[self.data[feature] == channel]
            
            sns.histplot(data=data, x='hour', stat='probability', kde=True, ax=ax)
            
            if len(data['hour']) > 1:
                kde = gaussian_kde(data['hour'], bw_method='scott')
                x_vals = np.linspace(data['hour'].min(), data['hour'].max(), 1000)
                y_vals = kde(x_vals)

                mean = np.mean(data['hour'])
                std_dev = np.sqrt(np.sum(y_vals * (x_vals - mean)**2) / np.sum(y_vals))
                
                max_prob_hour = x_vals[np.argmax(y_vals)]
                
                ax.axvline(max_prob_hour, color='red', linestyle='--')
                ax.annotate(f'Max prob: {max_prob_hour:.2f}', xy=(max_prob_hour, max(y_vals)),
                            xytext=(max_prob_hour + 0.5, max(y_vals) + 0.005))
                
                ax.annotate(f'STD: {std_dev:.2f}', xy=(0, max(y_vals)),
                            xytext=(0.5, max(y_vals) + 0.005))
            
            ax.set_title(f'{value:.2f}% Sample {channel.capitalize()} | (Probability) ')
            ax.set_xlabel('Hour')
            ax.set_ylabel('Probability')

        for i in range(num_channels, len(axes)):
            fig.delaxes(axes[i])

        plt.tight_layout()
        return fig
