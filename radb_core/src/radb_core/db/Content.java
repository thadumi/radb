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
import static java.util.stream.Collectors.*;
import static java.util.stream.IntStream.*;

import java.util.stream.Stream;

/**
 *
 * @author thadumi
 */
public class Content extends HashSet<List<String>>{
    
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
        final List<Integer> tmp = new ArrayList<>(indexes.length);
        for(int i : indexes) tmp.add(i);
        
        return getColumns(tmp);
    }
    
    public Stream<List<String>> getColumns(List<Integer> indexes) {
        return stream().map(row -> {
            final List<String> tmp = new ArrayList<>();
            //range(0, indexes.size())
            //         .forEach(i -> tmp.add(row.get(indexes.get(i))));
            indexes.forEach(i -> tmp.add(row.get(i)));
            return tmp;
        });
    }
}
