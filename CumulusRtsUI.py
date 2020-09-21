
# Java
import java
import javax
from java.lang import *

# Python
import os
import sys
import json
import argparse
import tempfile
import subprocess
import jarray

# HEC
import hec
from hec.heclib.util import HecTime

# Some constants
true = hec.script.Constants.TRUE
false = hec.script.Constants.FALSE
script_name = "CumulusRtsUI.py"                                 # This script name because __file__ doesn't work in CAVI env
cellsize = 2000
url_basins = "https://api.rsgis.dev/development/cumulus/basins"
url_products = "https://api.rsgis.dev/development/cumulus/products"
url_downloads = "https://api.rsgis.dev/development/cumulus/downloads"

'''Try importing hec2 package.  An exception is thrown if not in CWMS CAVI or
RTS CAVI.  This will determine if this script runs in the CAVI or other environment.
ClientAppCheck.haveClientApp() was tried but does not provide expected results.

If we are not in the CAVI environment, then we need to get the provided arguments
from this script because we will call it again outsid the CAVI environment.
'''
try:
    import hec2
    cavi_env = true
except ImportError as ex:
    print ex
    cavi_env = false


# CAVI Status class
class CaviStatus():
    '''
    '''
    def get_working_dir(self):
        '''
        Get the working directory, CWMS_HOME.
        '''
        _rts = hec2.rts.client.RTS.getRTS()
        wd = _rts.getWorkingDir()
        return wd

    def is_watershed_open(self):
        '''
        Return a boolean if a watershed is open
        '''
        return hec2.rts.script.RTS.isWatershedOpened()

    def get_watershed(self):
        '''
        Return the watershed object
        '''
        return hec2.rts.script.RTS.getWatershed()

    def get_project_directory(self):
        '''
        Get the open watershed and return its project directory
        '''
        _watershed = hec2.rts.script.RTS.getWatershed()
        pd = _watershed.getProjectDirectory()
        return pd

    def get_database_directory(self):
        '''
        Get the open watershed and return its project database directory
        '''
        _watershed = hec2.rts.script.RTS.getWatershed()
        _dir = _watershed.getProjectDirectory()
        _list = _dir.split(os.sep)[:-2]
        _list.append('database')
        _path = os.sep.join(_list)
        return _path

    def get_data_timewindow(self):
        '''
        '''
        _watershed = hec2.rts.script.RTS.getWatershed()
        wtw = _watershed.getDataTimeWindow()
        return wtw

    def get_current_module(self):
        '''
        '''
        return hec2.rts.script.RTS.getCurrentModule()

    def get_timewindow(self):
        '''
        Get the selected module and return its timewindow as a tuple of times.
        Results in start time and end time.
        '''
        _rtstab = hec2.rts.script.RTS.getCurrentModule()
        if isinstance(_rtstab, hec2.rts.ui.ForecastTab):
            if _rtstab.getForecast() == None:
                return None

        _list = list()
        for _tw in _rtstab.getTimeWindowString().split(";"):
            if (_tw == '' or _tw == None):
                return None

            _list.append(_tw)
        return tuple(_list)

    def get_selected_forecast(self):
        '''
        '''
        return hec2.rts.script.Forecast.getSelectedForecast()

    def get_run_timewindow(self):
        '''
        Get the selected forecast and return its timewindow as a tuple of HecTime.
        Results in start time, forecast time, and end time
        '''
        _forecast = hec2.rts.script.Forecast.getSelectedForecast()
        if _forecast != None:
            _list = list()
            for _tw in _forecast.getRunTimeWindow().toString().split(";"):
                _t = HecTime(_tw, HecTime.MINUTE_GRANULARITY)
                _list.append(_t)
            return tuple(_list)
        else:
            return None

    def get_forecast_dss(self):
        '''
        Get the selected forecast and return the forecast.dss
        '''
        _forecast = hec2.rts.script.Forecast.getSelectedForecast()
        if _forecast != None:
            dssfn = _forecast.getForecastDSSFilename()
            return dssfn
        else:
            return None

#if not cavi_env:
# Look and feel class
class LookAndFeel():
    '''Set the look and feel of the UI.  Execute before the objects are created.//n
    Takes one argument for the name of the look and feel class.
    '''
    def __init__(self, name):
        for info in javax.swing.UIManager.getInstalledLookAndFeels():
            if info.getName() == name:
                javax.swing.UIManager.setLookAndFeel(info.getClassName())

# File chooser class
class FileChooser(javax.swing.JFileChooser):
    '''Java Swing JFileChooser allowing for the user to select the dss file
    for output.
    '''
    def __init__(self, output_path):
        super(FileChooser, self).__init__()

        self.output_path = output_path

        self.setFileSelectionMode(javax.swing.JFileChooser.FILES_ONLY)
        
        self.allow = ['dss']
        self.destpath = None
        self.filetype = None
        self.current_dir = None
        self.title = None

        self.set_dialog_title(self.title)
        self.set_multi_select(false)
        self.set_hidden_files(false)
        self.set_file_type("dss")
        self.set_filter("HEC-DSS File ('*.dss')", "dss")
        
    def show(self):
        return_val = self.showSaveDialog(self)
        if self.destpath == None or self.filetype == None:
            return_val == javax.swing.JFileChooser.CANCEL_OPTION
        if return_val == javax.swing.JFileChooser.APPROVE_OPTION:
            self.approve_option()
        elif return_val == javax.swing.JFileChooser.CANCEL_OPTION:
            self.cancel_option()
        elif return_val == javax.swing.JFileChooser.ERROR_OPTION:
            self.error_option()
    
    def set_dialog_title(self, t):
        self.setDialogTitle(t)

    def set_current_dir(self, d):
        self.setCurrentDirectory(d)

    def set_multi_select(self, b):
        self.setMultiSelectionEnabled(b)
        
    def set_hidden_files(self, b):
        self.setFileHidingEnabled(b)

    def set_file_type(self, type):
        if type.lower() in self.allow:
            self.filetype = type.lower()
        
    def set_filter(self, desc, *ext):
        self.remove_filter(self.getChoosableFileFilters())
        filter = javax.swing.filechooser.FileNameExtensionFilter(desc, ext)
        filter_desc = [d.getDescription() for d in self.getChoosableFileFilters()]
        if not desc in filter_desc:
            self.addChoosableFileFilter(filter)
    
    def set_destpath(self, r):
        self.destpath = r

    def remove_filter(self, filter):
        # [self.removeChoosableFileFilter(f) for f in filter if f.getDescription() != 'All Files']
        [self.removeChoosableFileFilter(f) for f in filter]
        
    def get_files(self):
        files = [f for f in self.getSelectedFiles()]
        return files
    
    def cancel_option(self):
        for _filter in self.getChoosableFileFilters():
            self.removeChoosableFileFilter(_filter)

    def error_option(self):
        pass
    
    def approve_option(self):
        selected_file = self.getSelectedFile().getPath()
        # Send this on to a config file on the user's APPDATA
        with open(os.path.join(os.getenv('APPDATA'), "cumulus.config"), 'w+b') as f:
            f.write(selected_file)
        self.output_path.setText(selected_file)

# Java time formatter
class TimeFormatter():
    ''' Java time formatter/builder dealing with different date time formats '''
    def __init__(self, zid=java.time.ZoneId.of("UTC")):
        self.zid = zid
        self.fb = self.format_builder()

    def format_builder(self):
        fb = java.time.format.DateTimeFormatterBuilder()
        fb.parseCaseInsensitive()
        fb.appendPattern("[[d][dd]MMMyyyy[[,] [Hmm[ss]][H:mm[:ss]][HHmm][HH:mm[:ss]]]]" + \
            "[[d][dd]-[M][MM][MMM]-yyyy[[,] [Hmm[ss]][H:mm[:ss]][HHmm][HH:mm[:ss]]]]" + \
            "[yyyy-[M][MM][MMM]-[d][dd][['T'][ ][Hmm[ss]][H:mm[:ss]][HHmm[ss]][HH:mm[:ss]]]]")
        return fb.toFormatter()

    def iso_instant(self):
        return java.time.format.DateTimeFormatter.ISO_INSTANT
        
    def parse_local_date_time(self,t):
        return java.time.LocalDateTime.parse(t,self.fb)

    def parse_zoned_date_time(self,t, z):
        ldt = self.parse_local_date_time(t)
        return java.time.ZonedDateTime.of(ldt, z)

# Define something to download the DSS and process
def download_dss(dss_url, dss_out):
    print "DSS URL: " + dss_url
    print "DSS OUT: " + dss_out

    hec.heclib.util.Heclib.zset('DSSV', '', 6)
    dssin = None
    temp_file = None
    result = false
    try:
        # Create input stream reader to read the file
        url = java.net.URL(dss_url)
        urlconnect = url.openConnection()
        response_code = urlconnect.getResponseCode()
        if response_code == 200:
            input_stream = urlconnect.getInputStream()
            tempfile = java.nio.file.Files.createTempFile("", ".dss")
            java.nio.file.Files.copy(input_stream,
                tempfile,
                java.nio.file.StandardCopyOption.REPLACE_EXISTING
                )
        # Process the DSS file
            tempfile_string = tempfile.toString()
            if os.path.exist(os.path.dirname(tempfile_string)):
                dssin = hec.heclib.dss.HecDss.open(tempfile_string)
                for pathname in dssin.getCatalogedPathnames():
                    grid_container = dssin.get(pathname)
                    grid_data = grid_container.getGridData()
                    hec.heclib.grid.GridUtilities.storeGridToDss(dss_out, pathname, grid_data)
                result = true
        else:
            result = false
    except java.io.IOException as ex:
        raise Exception(ex)
    except hec.hecmath.DSSFileException, ex:
        raise Exception(ex)
    finally:
        input_stream.close()
        if dssin: dssin.done()

        return result

# Cumulus UI class
class CumulusUI(javax.swing.JFrame):
    '''Java Swing used to create a JFrame UI.  On init the objects will be
    populated with information derived from URL requests to CUMULUS and
    the open CWMS watershed.
    '''
    def __init__(self, arg_dict):
        super(CumulusUI, self).__init__()

        # Load argument from the command line
        self.start_time = arg_dict['start_time']
        self.end_time = arg_dict['end_time']
        self.dss_path = arg_dict['dss_path']
        self.cwms_home = arg_dict['cwms_home']
        self.config = arg_dict['config']

        # Get the DSS Path if one was saved in the "cumulus.config" file
        if os.path.isfile(self.config):
            with open(os.path.join(os.getenv('APPDATA'), "cumulus.config")) as f:
                _path = f.read()
                if _path:
                    self.dss_path = _path

        # Get the basins and products, load JSON, create lists for JList, and create dictionaries
        self.basin_download = json.loads(self.http_get(url_basins))        
        self.jlist_basins = ["{}:{}".format(b['office_symbol'], b['name']) for b in self.basin_download]
        self.basin_meta = dict(zip(self.jlist_basins, self.basin_download))
        self.jlist_basins.sort()

        self.product_download = json.loads(self.http_get(url_products))
        self.jlist_products = ["{}".format(p['name'].replace("_", " ").title()) for p in self.product_download]
        self.product_meta = dict(zip(self.jlist_products, self.product_download))
        self.jlist_products.sort()

        btn_submit = javax.swing.JButton()
        lbl_start_date = javax.swing.JLabel()
        lbl_end_date = javax.swing.JLabel()
        self.txt_select_file = javax.swing.JTextField()
        btn_select_file = javax.swing.JButton()
        lbl_origin = javax.swing.JLabel()
        lbl_extent = javax.swing.JLabel()
        self.txt_originx = javax.swing.JTextField()
        self.txt_originy = javax.swing.JTextField()
        self.txt_extentx = javax.swing.JTextField()
        self.txt_extenty = javax.swing.JTextField()
        lbl_select_file = javax.swing.JLabel()
        comma1 = javax.swing.JLabel()
        comma2 = javax.swing.JLabel()
        paren_l1 = javax.swing.JLabel()
        paren_l2 = javax.swing.JLabel()
        paren_r1 = javax.swing.JLabel()
        paren_r2 = javax.swing.JLabel()
        self.txt_start_time = javax.swing.JTextField()
        self.txt_end_time = javax.swing.JTextField()

        jScrollPane1 = javax.swing.JScrollPane()
        self.lst_product = javax.swing.JList()
        self.lst_product = javax.swing.JList(self.jlist_products, valueChanged = self.choose_product)
        
        jScrollPane2 = javax.swing.JScrollPane()
        self.lst_watershed = javax.swing.JList()
        self.lst_watershed = javax.swing.JList(self.jlist_basins, valueChanged = self.choose_watershed)

        self.setDefaultCloseOperation(javax.swing.WindowConstants.DISPOSE_ON_CLOSE)
        self.setTitle("Cumulus CAVI UI")
        self.setLocation(java.awt.Point(10, 10))
        self.setLocationByPlatform(true)
        self.setName("CumulusCaviUi")
        self.setResizable(false)

        btn_submit.setFont(java.awt.Font("Tahoma", 0, 18))
        btn_submit.setText("Submit")
        btn_submit.actionPerformed = self.submit

        lbl_start_date.setText("Start Date/Time")

        lbl_end_date.setText("End Date/Time")

        self.txt_select_file.setToolTipText("FQPN to output file (.dss)")

        btn_select_file.setText("...")
        btn_select_file.setToolTipText("Select File...")
        btn_select_file.actionPerformed = self.select_file

        lbl_origin.setText("Minimum (x,y):")

        lbl_extent.setText("Maximum (x,y):")

        self.txt_originx.setToolTipText("Minimum X")

        self.txt_originy.setToolTipText("Minimum Y")

        self.txt_extentx.setToolTipText("Maximum X")

        self.txt_extenty.setToolTipText("Maximum Y")

        lbl_select_file.setText("Output File Location")

        comma1.setFont(java.awt.Font("Tahoma", 0, 12))
        comma1.setText(",")

        comma2.setFont(java.awt.Font("Tahoma", 0, 12))
        comma2.setText(",")

        paren_l1.setText("(")

        paren_l2.setText("(")

        paren_r1.setText(")")

        paren_r2.setText(")")

        self.txt_start_time.setToolTipText("Start Time (yyyy-mm-ddThh:mm:ss)")
        self.txt_end_time.setToolTipText("End Time")

        self.lst_product.setBorder(javax.swing.BorderFactory.createTitledBorder(None, "Available Products", javax.swing.border.TitledBorder.CENTER, javax.swing.border.TitledBorder.TOP, java.awt.Font("Tahoma", 0, 14)))
        self.lst_product.setFont(java.awt.Font("Tahoma", 0, 14))
        jScrollPane1.setViewportView(self.lst_product)
        self.lst_product.getAccessibleContext().setAccessibleName("Available Products")
        self.lst_product.getAccessibleContext().setAccessibleParent(jScrollPane2)

        self.lst_watershed.setBorder(javax.swing.BorderFactory.createTitledBorder(None, "Available Watersheds", javax.swing.border.TitledBorder.CENTER, javax.swing.border.TitledBorder.TOP, java.awt.Font("Tahoma", 0, 14)))
        self.lst_watershed.setFont(java.awt.Font("Tahoma", 0, 14))
        self.lst_watershed.setSelectionMode(javax.swing.ListSelectionModel.SINGLE_SELECTION)
        jScrollPane2.setViewportView(self.lst_watershed)

        layout = javax.swing.GroupLayout(self.getContentPane())
        self.getContentPane().setLayout(layout)
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                    .addComponent(lbl_select_file)
                    .addComponent(jScrollPane1)
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                        .addComponent(paren_l1)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(lbl_origin)
                            .addGroup(layout.createSequentialGroup()
                                .addComponent(self.txt_originx, javax.swing.GroupLayout.PREFERRED_SIZE, 65, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(comma1, javax.swing.GroupLayout.PREFERRED_SIZE, 5, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(self.txt_originy, javax.swing.GroupLayout.PREFERRED_SIZE, 65, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(paren_r1)))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                        .addComponent(paren_l2)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(lbl_extent)
                            .addGroup(layout.createSequentialGroup()
                                .addComponent(self.txt_extentx, javax.swing.GroupLayout.PREFERRED_SIZE, 65, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(comma2)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(self.txt_extenty, javax.swing.GroupLayout.PREFERRED_SIZE, 65, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(paren_r2))))
                    .addComponent(jScrollPane2)
                    .addGroup(layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                            .addComponent(btn_submit)
                            .addComponent(self.txt_select_file, javax.swing.GroupLayout.PREFERRED_SIZE, 377, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(btn_select_file))
                    .addGroup(layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(lbl_start_date)
                            .addComponent(self.txt_start_time, javax.swing.GroupLayout.PREFERRED_SIZE, 140, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                            .addGroup(layout.createSequentialGroup()
                                .addComponent(lbl_end_date)
                                .addGap(70, 70, 70))
                            .addComponent(self.txt_end_time, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.PREFERRED_SIZE, 140, javax.swing.GroupLayout.PREFERRED_SIZE))))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        )
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addGap(25, 25, 25)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(lbl_start_date)
                    .addComponent(lbl_end_date))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(self.txt_start_time, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(self.txt_end_time, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addGap(18, 18, 18)
                .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, 201, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(18, 18, 18)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(lbl_extent)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(self.txt_extentx, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(self.txt_extenty, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(comma2)
                            .addComponent(paren_l2)
                            .addComponent(paren_r2)))
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(lbl_origin)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(self.txt_originx, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(self.txt_originy, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(comma1)
                            .addComponent(paren_l1)
                            .addComponent(paren_r1))))
                .addGap(39, 39, 39)
                .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 201, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(18, 18, Short.MAX_VALUE)
                .addComponent(lbl_select_file)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(self.txt_select_file, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(btn_select_file))
                .addGap(18, 18, 18)
                .addComponent(btn_submit)
                .addContainerGap())
        )
        self.txt_select_file.setText(self.dss_path)
        self.txt_start_time.setText(self.start_time)
        self.txt_end_time.setText(self.end_time)

        self.pack()
        self.setLocationRelativeTo(None)

    def http_get(self, url):
        try:
            url = java.net.URL(url)
            urlconnect = url.openConnection()
            # response_code = urlconnect.getResponseCode()
            br = java.io.BufferedReader(
                java.io.InputStreamReader(
                    urlconnect.getInputStream(), "UTF-8"
                )
            )
            s = br.readLine()
            br.close()
        except java.net.MalformedURLException() as ex:
            raise Exception(ex)
        except java.io.IOException as ex:
            raise Exception(ex)

        return s

    def http_post(self, json_string, url):
        try:
            # Get a connection and set the request properties
            url = java.net.URL(url)
            urlconnect = url.openConnection()
            urlconnect.setDoOutput(true)
            urlconnect.setRequestMethod("POST")
            urlconnect.setRequestProperty("Content-Type", "application/json; UTF-8")
            urlconnect.setRequestProperty("Accept", "application/json")
            # response_code = urlconnect.getResponseCode()
            # Write to the body
            bw = java.io.BufferedWriter(
                java.io.OutputStreamWriter(
                    urlconnect.getOutputStream()
                )
            )
            bw.write(json_string)
            bw.flush()
            bw.close()
            # Read the request until file is 100% and then process the DSS file
            br = java.io.BufferedReader(
                java.io.InputStreamReader(
                    urlconnect.getInputStream(), "UTF-8"
                )
            )
            response = br.readLine()
            br.close()
        except java.net.MalformedURLException() as ex:
            raise Exception(ex)
        except java.io.IOException as ex:
            raise Exception(ex)

        return response

    def json_build(self):
        # Get the data in JSON
        conf = {
            'datetime_start': None,
            'datetime_end': None,
            'basin_id': None,
            'product_id': None,
            }

        try:
            tf = TimeFormatter()
            tz = tf.zid
            st = tf.parse_zoned_date_time(self.txt_start_time.getText(), tz)
            et = tf.parse_zoned_date_time(self.txt_end_time.getText(), tz)
        except java.time.format.DateTimeParseException as ex:
            javax.swing.JOptionPane.showMessageDialog(
                    None,
                    "DateTimeParseException\n\nCheck date formats.",
                    "Exception",
                    javax.swing.JOptionPane.ERROR_MESSAGE)
            return None

        conf['datetime_start'] = st.format(tf.iso_instant())
        conf['datetime_end'] = et.format(tf.iso_instant())

        selected_watershed = self.lst_watershed.getSelectedValue()
        selected_products = self.lst_product.getSelectedValues()

        if not selected_watershed == None:
            watershed_id = self.basin_meta[selected_watershed]['id']
            conf['basin_id'] = watershed_id
        else:
            javax.swing.JOptionPane.showMessageDialog(
                None,
                "No Watershed Selected",
                "Exception",
                javax.swing.JOptionPane.INFORMATION_MESSAGE)
            return None
        
        product_ids = list()
        if len(selected_products) > 0:
            for p in selected_products:
                product_ids.append(self.product_meta[p]['id'])
                conf['product_id'] = product_ids
        else:
            javax.swing.JOptionPane.showMessageDialog(
                None,
                "No Products Selected",
                "Exception",
                javax.swing.JOptionPane.INFORMATION_MESSAGE)
            return None

        return json.dumps(conf)

    def choose_product(self, event):
        '''The event here is a javax.swing.event.ListSelectionEvent because
        is comes from a Jlist.  Use getValueIsAdjusting() to only get the
        mouse up value.
        '''
        index = self.lst_product.selectedIndex
        if not event.getValueIsAdjusting():
            pass
            # print self.product_meta[self.lst_product.getSelectedValues()]

    def choose_watershed(self, event):
        '''The event here is a javax.swing.event.ListSelectionEvent because
        is comes from a Jlist.  Use getValueIsAdjusting() to only get the
        mouse up value.
        '''
        index = self.lst_watershed.selectedIndex
        if not event.getValueIsAdjusting():
            _dict = self.basin_meta[self.lst_watershed.getSelectedValue()]
            self.txt_originx.setText(str(_dict['x_min']))
            self.txt_originy.setText(str(_dict['y_min']))
            self.txt_extentx.setText(str(_dict['x_max']))
            self.txt_extenty.setText(str(_dict['y_max']))

    def select_file(self, event):
        '''Provide the user a JFileChooser to select the DSS file data is to download to.

        event is a java.awt.event.ActionEvent
        '''
        fc = FileChooser(self.txt_select_file)
        fc.title = "Select Output DSS File"
        _dir = os.path.dirname(self.dss_path)
        fc.set_current_dir(java.io.File(_dir))
        fc.show()

    def submit(self, event):
        '''Collect user inputs and initiate download of DSS files to process.

        event is a java.awt.event.ActionEvent
        '''
        post_result = None
        get_result = None
        json_string = None

        # Build the JSON from the UI inputs and POST if we have JSON
        json_string = self.json_build()

        if not json_string == None:
            post_result = self.http_post(json_string, url_downloads)
            json_post_result = json.loads(post_result)
            id = json_post_result['id']

            id = "28f11344-e90b-4671-9466-389a26175456"                         # THIS IS FOR TESTING TO GET A 100% result


        else:
            javax.swing.JOptionPane.showMessageDialog(
                None,
                "POST result is 'None'",
                "Exception",
                javax.swing.JOptionPane.ERROR_MESSAGE
            )

        # Check the POST result from above and GET the result to process on
        if not post_result == None:
            get_result = self.http_get("/".join([url_downloads, id]))
            json_get_result = json.loads(get_result)
            print json_get_result                                               # REMOVE AFTER TESTING
        else:
            javax.swing.JOptionPane.showMessageDialog(
                None,
                "GET result is 'None'",
                "Exception",
                javax.swing.JOptionPane.ERROR_MESSAGE
            )

        # Process the GET result and loop until 100% (file ready for download)
        if not get_result == None:
            timeout = 0
            while timeout < 15:
                get_result = self.http_get("/".join([url_downloads, id]))
                json_get_result = json.loads(get_result)
                progress = json_get_result['progress']                          #100%
                stat = json_get_result['status']                                #SUCCESS
                fname = json_get_result['file']                                 # not null

                fname = "https://api.rsgis.dev/cumulus/download/dss/precip_test.dss"        # THIS IS TO TEST

                if int(progress) == 100 and stat == 'SUCCESS':                  # May add file check to make sure not None
                    result = download_dss(fname, self.txt_select_file.getText())
                    if not result:
                        javax.swing.JOptionPane.showMessageDialog(
                            None,
                            "Downloading and processing the DSS file failed!",
                            "Failed DSS Processing",
                            javax.swing.JOptionPane.ERROR_MESSAGE
                        )
                    break
                else:
                    print stat
                    Thread.sleep(2000)
                timeout += 1
        else:
            javax.swing.JOptionPane.showMessageDialog(
                None,
                "GET result is 'None'",
                "Exception",
                javax.swing.JOptionPane.ERROR_MESSAGE
            )


def main():
    ''' The main section to determine is the script is executed within or
    outside of the CAVI environment
    '''
    if cavi_env:                                                                # This is all the stuff to do if in the CAVI
        tw = CaviStatus().get_timewindow()
        if tw == None:
        	raise Exception("No forecast open on Modeling tab to get a timewindow.")
        db = os.path.join(CaviStatus().get_database_directory(), "grid.dss")
        cwms_home = CaviStatus().get_working_dir()
        common_exe = os.path.join(os.path.split(cwms_home)[0], "common", "exe")
        cumulus_config = os.path.join(os.getenv("APPDATA"), "cumulus.config")
        this_script = os.path.join(CaviStatus().get_project_directory(), "scripts", script_name)
        cmd = "@PUSHD {pushd}\n"
        cmd += "Jython.bat {script} "
        cmd += "'{start}' '{end}' '{dss}' '{home}' '{config}'"
        cmd = cmd.format(pushd=common_exe, script=this_script, start=tw[0],
            end=tw[1], dss=db, home=cwms_home, config=cumulus_config
            )
        print cmd
        # Create a temporary file that will be executed outside the CAVI env
        batfile = tempfile.NamedTemporaryFile(mode='w+b', suffix='.cmd', delete=false)
        batfile.write(cmd)
        batfile.close()
        p = subprocess.call(batfile.name)
    else:                                                                       # This is all the stuff to do if initiated outside the CAVI environment
        args = sys.argv[1:]
        if len(args) < 5:
            raise Exception("Need more arguments")
        keys = ['start_time', 'end_time', 'dss_path', 'cwms_home', 'config']
        ordered_dict = dict(zip(keys, args))

        # Set the look and feel
        # Metal, Nimbus, CDE/Motif, Windows, or Windows Classic
        LookAndFeel("Nimbus")

        cui = CumulusUI(ordered_dict)
        cui.setVisible(true)

if __name__ == "__main__":
    # DELETE THIS LIST.  ONLY FOR TESTING
    sys.argv[1:] = ["28AUG2020, 12:00", "31AUG2020, 12:00", "D:/WS_CWMS/lrn-m3000-v31-pro/database/grid.dss", "C:/app/CWMS/CWMS-Production/CAVI", "C:/Users/h3ecxjsg/AppData/Roaming/cumulus.config"]
    # DELETE THIS LIST.  ONLY FOR TESTING
    main()