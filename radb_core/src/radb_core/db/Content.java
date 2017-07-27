/*
 *  This file is part of RADB Project created by Dumitrescu Theodor A. and Calvi Luigino.
 *
 *  Foobar is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.

 *  RADB is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.

 *  You should have received a copy of the GNU General Public License
 *  along with RADB.  If not, see <http://www.gnu.org/licenses/>.
 */
package radb_core.db;

import java.util.Arrays;
import java.util.Collection;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Objects;
import java.util.Set;
import java.util.stream.Stream;
import static java.util.stream.Collectors.*;

import static radb_core.util.Collections.*;
import static radb_core.util.Checker.*;

public class Content extends HashSet<List<String>> implements Cloneable{
    
    public static final String EMPTY = "$NULL$";
    
    
    private int nrElem;
    
    
    Content(Collection<List<String>> c) {
        //super(c);
        super(c.size());
        
        /*Iterator i = c.iterator();
        
        if(i.hasNext())
            nrElem = ((List<String>) i.next()).size();
        else nrElem = -1;
        */
        nrElem = -1;
        
        c.stream().forEach(this::add);
    }
    
    Content() {
        nrElem = -1;
    }
    
    public static Content emptyContent() {
        return new Content();
    }
    
    public static Content of(String content) {
        requireNonNull(content, "The content can't be null");
        throwIf(content, String::isEmpty, "The content is as string with at least one row");
        
        Content c = emptyContent();
        
        Stream.of(content.split("\n"))
              .forEach(c::add);
        
        return c;
    }
    
    public static Content of(Collection<List<String>> content) {
        requireNonNull(content, "The content can't be null");
        
        return new Content(content);
    }
    
    
    public boolean add(String row) {
        return add(Arrays.asList(row.split(", ")));
    }

    
    
    @Override
    public boolean add(List<String> e) {
        throwIf(e , 
                arg -> Objects.isNull(arg) || arg.isEmpty(), 
                "The argument can't be null or empty");
        
        
        if(nrElem == -1 && add(e)) {
            nrElem = e.size();
            return true;
        }
        
        throwIf(e, 
                arg -> arg.size() != nrElem,
                "Can't add a record that hasn't " + nrElem + " elements");
        
        return super.add(e);
    }
    
    Stream<List<String>> getColumns(int ... indexes) {
        return getColumns(toList(indexes));
    }
    
    Stream<List<String>> getColumns(List<Integer> indexes) {
        return stream().map(row ->
            indexes.stream().map(i -> row.get(i))
                            .collect(toList())
            );
    }
    
    public Content intersection(Set< ? extends List<String>> other) {
        Set<List<String>> tmp = clone();
        tmp.retainAll(other);
        
        return (Content) tmp;
    }
    
    public Content difference(Set< ? extends List<String>> other) {
        Set<List<String>> tmp = clone();
        tmp.removeAll(other);
        
        return (Content) tmp;
    }
    
    public Content union(Set<? extends List<String>> other) {
        Set<List<String>> tmp = clone();
        tmp.addAll(other);
        
        return (Content) tmp;   
    }

    @Override
    public Content clone() {
        return new Content(stream().collect(toList()));
    }
    
    @Override
    public String toString() {
        return stream()
                   .map(row -> row.stream().collect(joining(", ", "", "")))
                   .collect(joining("\n", "", ""));
    }
    
}
