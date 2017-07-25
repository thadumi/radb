/*
 *  This file is part of RADB Project create by Dumitrescu Theodor A. and Calvi Luigino.
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

import java.util.List;
import static java.util.stream.Collectors.*;
import java.util.stream.Stream;
/**
 *
 * @author thadumi
 */
public class Utilities {
    private Utilities() {}
    
    public static List<Object> cast(Stream<String> l) {
        return l.map(e -> StringEvaluator.cast(e).get() )
                .collect(toList());
                
    }
    
    public static List<Object> cast(List<String> l) {
        return cast(l.stream());
    }
    
    public static List<String> toString(Stream<Object> l) {
        return l.map(e -> e.toString())
                .collect(toList());
    }
    
    public static List<String> toString(List<Object> l) {
        return toString(l.stream());
    }
}
