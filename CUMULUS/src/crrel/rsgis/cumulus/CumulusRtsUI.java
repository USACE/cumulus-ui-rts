/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package crrel.rsgis.cumulus;

/**
 *
 * @author h3ecxjsg
 */
public class CumulusRtsUI extends javax.swing.JFrame {

    /**
     * Creates new form CumulusRtsUi
     */
    public CumulusRtsUI() {
        initComponents();
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        btn_submit = new javax.swing.JButton();
        chk_ncep_rtma_precip = new javax.swing.JCheckBox();
        chk_ncep_rtma_airtemp = new javax.swing.JCheckBox();
        chk_nohrsc_snodas_snowdepth = new javax.swing.JCheckBox();
        lbl_start_date = new javax.swing.JLabel();
        lbl_end_date = new javax.swing.JLabel();
        txt_select_file = new javax.swing.JTextField();
        btn_select_file = new javax.swing.JButton();
        lbl_origin = new javax.swing.JLabel();
        lbl_extent = new javax.swing.JLabel();
        txt_originx = new javax.swing.JTextField();
        txt_originy = new javax.swing.JTextField();
        txt_extentx = new javax.swing.JTextField();
        txt_extenty = new javax.swing.JTextField();
        lbl_product = new javax.swing.JLabel();
        lbl_select_file = new javax.swing.JLabel();
        comma1 = new javax.swing.JLabel();
        comma2 = new javax.swing.JLabel();
        paren_l1 = new javax.swing.JLabel();
        paren_l2 = new javax.swing.JLabel();
        paren_r1 = new javax.swing.JLabel();
        paren_r2 = new javax.swing.JLabel();
        txt_start_time = new javax.swing.JTextField();
        txt_end_time = new javax.swing.JTextField();
        jScrollPane1 = new javax.swing.JScrollPane();
        lst_watershed = new javax.swing.JList();

        setDefaultCloseOperation(javax.swing.WindowConstants.DISPOSE_ON_CLOSE);
        setTitle("Cumulus CAVI UI");
        setLocation(new java.awt.Point(10, 10));
        setLocationByPlatform(true);
        setName("CumulusCaviUi"); // NOI18N
        setResizable(false);

        btn_submit.setFont(new java.awt.Font("Tahoma", 0, 18)); // NOI18N
        btn_submit.setText("Submit");
        btn_submit.setActionCommand("submit");

        chk_ncep_rtma_precip.setText("NCEP RTMA Precipitation");

        chk_ncep_rtma_airtemp.setText("NCEP RTMA Airtemp");

        chk_nohrsc_snodas_snowdepth.setText("SNODAS Snow Depth");

        lbl_start_date.setText("Start Date/Time");

        lbl_end_date.setText("End Date/Time");

        txt_select_file.setText("C:\\projects\\CWMS\\database\\grid.dss");
        txt_select_file.setToolTipText("FQPN to output file (.dss)");

        btn_select_file.setText("...");
        btn_select_file.setToolTipText("Select File...");

        lbl_origin.setText("Origin (x,y):");

        lbl_extent.setText("Extents (x,y):");

        txt_originx.setToolTipText("Origin X");

        txt_originy.setToolTipText("Origin Y");

        txt_extentx.setToolTipText("Extent X");

        txt_extenty.setToolTipText("Extent Y");

        lbl_product.setText("Products");

        lbl_select_file.setText("Output File Location");

        comma1.setFont(new java.awt.Font("Tahoma", 0, 12)); // NOI18N
        comma1.setText(",");

        comma2.setFont(new java.awt.Font("Tahoma", 0, 12)); // NOI18N
        comma2.setText(",");

        paren_l1.setText("(");

        paren_l2.setText("(");

        paren_r1.setText(")");

        paren_r2.setText(")");

        txt_start_time.setText("2020-12-16 12:00:00");
        txt_start_time.setToolTipText("Start Time (yyyy-mm-ddThh:mm:ss)");

        txt_end_time.setText("2020-12-16 12:00:00");
        txt_end_time.setToolTipText("End Time");

        lst_watershed.setBorder(javax.swing.BorderFactory.createTitledBorder(null, "Available Watersheds", javax.swing.border.TitledBorder.CENTER, javax.swing.border.TitledBorder.TOP, new java.awt.Font("Tahoma", 0, 14))); // NOI18N
        lst_watershed.setFont(new java.awt.Font("Tahoma", 0, 14)); // NOI18N
        lst_watershed.setSelectionMode(javax.swing.ListSelectionModel.SINGLE_SELECTION);
        jScrollPane1.setViewportView(lst_watershed);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap(25, Short.MAX_VALUE)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addGap(286, 286, 286)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                            .addGroup(layout.createSequentialGroup()
                                .addComponent(lbl_end_date)
                                .addGap(137, 137, 137))
                            .addComponent(txt_end_time, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.PREFERRED_SIZE, 140, javax.swing.GroupLayout.PREFERRED_SIZE)))
                    .addGroup(layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(lbl_start_date)
                            .addGroup(layout.createSequentialGroup()
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                                    .addComponent(btn_submit)
                                    .addComponent(txt_select_file, javax.swing.GroupLayout.PREFERRED_SIZE, 425, javax.swing.GroupLayout.PREFERRED_SIZE))
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(btn_select_file))
                            .addComponent(lbl_select_file)
                            .addGroup(layout.createSequentialGroup()
                                .addComponent(paren_l1)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                    .addComponent(lbl_origin)
                                    .addGroup(layout.createSequentialGroup()
                                        .addComponent(txt_originx, javax.swing.GroupLayout.PREFERRED_SIZE, 60, javax.swing.GroupLayout.PREFERRED_SIZE)
                                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                        .addComponent(comma1, javax.swing.GroupLayout.PREFERRED_SIZE, 5, javax.swing.GroupLayout.PREFERRED_SIZE)
                                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                        .addComponent(txt_originy, javax.swing.GroupLayout.PREFERRED_SIZE, 60, javax.swing.GroupLayout.PREFERRED_SIZE)
                                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                        .addComponent(paren_r1)))
                                .addGap(105, 105, 105)
                                .addComponent(paren_l2)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                    .addComponent(lbl_extent)
                                    .addGroup(layout.createSequentialGroup()
                                        .addComponent(txt_extentx, javax.swing.GroupLayout.PREFERRED_SIZE, 60, javax.swing.GroupLayout.PREFERRED_SIZE)
                                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                        .addComponent(comma2)
                                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                        .addComponent(txt_extenty, javax.swing.GroupLayout.PREFERRED_SIZE, 60, javax.swing.GroupLayout.PREFERRED_SIZE)
                                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                        .addComponent(paren_r2))))
                            .addComponent(txt_start_time, javax.swing.GroupLayout.PREFERRED_SIZE, 140, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addGroup(layout.createSequentialGroup()
                                .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 305, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addGap(18, 18, 18)
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                    .addComponent(chk_nohrsc_snodas_snowdepth)
                                    .addComponent(chk_ncep_rtma_precip)
                                    .addComponent(chk_ncep_rtma_airtemp)
                                    .addComponent(lbl_product))))
                        .addGap(25, 25, 25))))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addGap(25, 25, 25)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(lbl_start_date)
                    .addComponent(lbl_end_date))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(txt_start_time, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(txt_end_time, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addGap(30, 30, 30)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(lbl_product)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(chk_ncep_rtma_precip)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(chk_nohrsc_snodas_snowdepth, javax.swing.GroupLayout.PREFERRED_SIZE, 35, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(chk_ncep_rtma_airtemp))
                    .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 201, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addGap(18, 18, 18)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(lbl_extent)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(txt_extentx, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(txt_extenty, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(comma2)
                            .addComponent(paren_l2)
                            .addComponent(paren_r2)))
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(lbl_origin)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(txt_originx, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(txt_originy, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(comma1)
                            .addComponent(paren_l1)
                            .addComponent(paren_r1))))
                .addGap(18, 18, Short.MAX_VALUE)
                .addComponent(lbl_select_file)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(txt_select_file, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(btn_select_file))
                .addGap(26, 26, 26)
                .addComponent(btn_submit)
                .addGap(25, 25, 25))
        );

        pack();
        setLocationRelativeTo(null);
    }// </editor-fold>//GEN-END:initComponents

    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(CumulusRtsUI.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(CumulusRtsUI.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(CumulusRtsUI.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(CumulusRtsUI.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new CumulusRtsUI().setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton btn_select_file;
    private javax.swing.JButton btn_submit;
    private javax.swing.JCheckBox chk_ncep_rtma_airtemp;
    private javax.swing.JCheckBox chk_ncep_rtma_precip;
    private javax.swing.JCheckBox chk_nohrsc_snodas_snowdepth;
    private javax.swing.JLabel comma1;
    private javax.swing.JLabel comma2;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JLabel lbl_end_date;
    private javax.swing.JLabel lbl_extent;
    private javax.swing.JLabel lbl_origin;
    private javax.swing.JLabel lbl_product;
    private javax.swing.JLabel lbl_select_file;
    private javax.swing.JLabel lbl_start_date;
    private javax.swing.JList lst_watershed;
    private javax.swing.JLabel paren_l1;
    private javax.swing.JLabel paren_l2;
    private javax.swing.JLabel paren_r1;
    private javax.swing.JLabel paren_r2;
    private javax.swing.JTextField txt_end_time;
    private javax.swing.JTextField txt_extentx;
    private javax.swing.JTextField txt_extenty;
    private javax.swing.JTextField txt_originx;
    private javax.swing.JTextField txt_originy;
    private javax.swing.JTextField txt_select_file;
    private javax.swing.JTextField txt_start_time;
    // End of variables declaration//GEN-END:variables
}
