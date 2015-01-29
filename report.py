import os
import datetime
import logging as log
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.font_manager as fm
import numpy as np
import util
class Report:
    """Class that is used to store multiple reports, by level of gravity
    and can display them after the analysis is done.
    It also handles the saving of graphs by algorithm. Can save multiple graph,
    with multiple lines insede."""
    DEBUG = 0
    INFO = 1
    ERROR = 2
    CRITICAL = 3
    DIR_GRAPH = "graphs"
    def __init__(self):
        self.messages = { key: [] for key in (Report.DEBUG,Report.INFO,Report.ERROR,Report.CRITICAL) }
        self.graphs = {}
        self.time_format = md.DateFormatter("%Y-%m-%d %H:%M:%S")

    def store_message(self,level, message):
        if level not in self.messages: level = Report.INFO
        self.messages[level].append(message)
    
    def summary(self,tolog=True,tofile=None):
        """Return a summary of the reports. Basically all reports organized by level of 
        gravity. You can pass it a log = False to NOT print on the log output, and file
        name to where to write this report (append)."""
        if tolog is False and tofile is None:
            log.warning("Requested a summary without logging or file output. Weirdo !")
            return
        log.info("-" * 50)
        self.summary_log()
        if tofile: self.summary_file(tofile)
        log.info("-" * 50)

    def summary_log(self):
        for mess in self.messages[Report.DEBUG]:
            log.debug(mess)
        for mess in self.messages[Report.INFO]:
            log.info(mess)
        for mess in self.messages[Report.ERROR]:
            log.warning(mess)
        for mess in self.messages[Report.CRITICAL]:
            log.critical(mess)

    def summary_file(self,file):
        pass


    def add_curve(self,graph_name,name,data):
        """Call this to add a curve to a graph. Data
        must be in format [ (ts,value),(ts,value) ...]"""
        if graph_name not in self.graphs:
            self.graphs[graph_name] = {}
        self.graphs[graph_name][name] = data
    
    def save_graph(self,fname=None):
        """ save the graphs to .png files under the graph folder"""
        self.check_graph_dir()
        if len(self.graphs) == 0: 
            log.info("No graphs has been assigned by the algorithm.")
        if not fname: fname = generate_file_name()
        fname = os.path.join(self.DIR_GRAPH,fname) 
        fig = plt.figure(figsize=(7,13)) ## one graph per row
        legends = [] ## need to save ref's to legends
        row = 1
        for name,graph in self.graphs.items():
            sub = fig.add_subplot(len(graph),1,row)
            legends.append(self.generate_plot(sub,name,graph))
            row += 1
        fig.savefig(fname,format="png",transparent="False",
                    bbox_extra_artists=legends,bbox_inches="tight")
        log.info("Graph has been exported to {} .".format(fname))
            

    def generate_plot(self,subplot,name,graph):
        """ Generate a plot on the subplot object, in the row-th row,
        will be named "name" and contains the data in graph.
        It returns a legend for this plot. Needed when we save the plot
        to a file, otherwise the legend is cropped if placed outside the graph"""
        legends = []
        max_value = 0
        for curve,data in graph.items():
            x,y = zip(*data)
            x = self.transform_timestamps(x)
            subplot.plot(x,y)
            legends.append(curve)
        self.set_subplot_options(subplot,legends)
        lgd = subplot.legend(legends,fontsize="x-small",borderpad=0.5,
                        labelspacing=0.2,
                        loc="center right",
                        bbox_to_anchor=(1.25,0.5))
        return lgd
        

    def set_subplot_options(self,subplot,legends,yticks=13,scale=0.05):
        """Set diverses options regarding the labels, xaxis, yaxis etc
        yticks is the number of ticks we want on the y-axis.
        scale is if we want to have the graph a bit higher on the bottom & top
        it will be operated like this : min = min * (1-scale). same for max"""
        subplot.xaxis.set_major_formatter(self.time_format)
        subplot.set_xlabel("Time")
        subplot.set_ylabel("Value")
        plt.xticks(rotation = 25)
        start,stop = subplot.get_ylim()
        subplot.set_ylim(int(start*(1-scale)),int(stop*(1+scale)))
        ticks = np.arange(start,stop,int((stop-start)/yticks))
        subplot.set_yticks(ticks)
        #subplot.set_ylim(start,int(stop*1.1))
        

    def transform_timestamps(self,ts):
        """transform the timestamps into datenum of matplotlib
        so they can be adequatly displayed on the graph"""
        newts = []
        for t in ts:
            datet = datetime.datetime.fromtimestamp(t)
            newts.append(md.date2num(datet))
        return newts

    def check_graph_dir(self):
        """check if the graph folder exists and creates it if not"""
        d = os.path.join(os.path.dirname(__file__),self.DIR_GRAPH) 
        try:
            if not os.path.exists(d):
                os.makedirs(d)
        except IOError as e:
            log.error("Error while creating the folder for the graphs. {}".format(e))
            exit(1)
        
    def generate_file_name(self):
        """ generate an unique file name for a graph"""
        return util.now2str() + "_report.png"
