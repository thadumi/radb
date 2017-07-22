/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package radb_core.storage;

import java.io.File;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.nio.file.Files;
import java.nio.file.StandardOpenOption;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import radb_core.db.Content;
import radb_core.db.Header;

/**
 *
 * @author thadumi
 */
public class TableIO {
    /*public static Table readTable(File table) {
        Table t = null;
        try {
            List<String> lines = Files.readAllLines(table.toPath());
            
            Header h = new Header(lines.get(0));
            Content c = new Content();
            lines.stream().forEach(l -> c.addRow(l));
            
            t = new Table(table.getName(), h, c);
            
        } catch (IOException ex) {
            Logger.getLogger(TableIO.class.getName()).log(Level.SEVERE, null, ex);
        }
        return t;   
    }
    
    public static void writeTable(Table t, File location) {
        StringBuilder sb = new StringBuilder();
        sb.append(t.getHeader())
          //.append("\n")
          .append(t.getContent());
        
        try {
            Files.write(location.toPath(), sb.toString().getBytes("utf-8") , StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING);
        } catch (UnsupportedEncodingException ex) {
            Logger.getLogger(TableIO.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(TableIO.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        
        
    }*/
}
