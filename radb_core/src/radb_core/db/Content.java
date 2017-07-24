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

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import static java.util.stream.Collectors.*;

import java.util.stream.Stream;

/**
 *
 * @author Dumitrescu Theodor A.
 */
public class Content extends HashSet<List<String>> implements Cloneable{
    
    public Content(String content) {
        Stream.of(content.split("\n"))
              .forEach(this::add);
    }
    
    public Content(List<List<String>> c) {
        super(c);
    }
    
    public Content() {
        this("");
    }
        

    
    @Override
    public String toString() {
        return stream()
                   .map(row -> row.stream().collect(joining(", ", "", "")))
                   .collect(joining("\n", "", ""));
    }

    public boolean add(String row) {
        return add(Arrays.asList(row.split(", ")));
    }
    
    public Stream<List<String>> getColumns(int ... indexes) {
        return getColumns(Arrays.stream(indexes).boxed().collect(toList()));
    }
    
    public Stream<List<String>> getColumns(List<Integer> indexes) {
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
    
}
