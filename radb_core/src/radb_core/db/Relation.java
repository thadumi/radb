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
import java.util.Collections;
import java.util.List;
import static java.util.Objects.*;
import java.util.Set;
import static java.util.stream.Collectors.*;
import static java.util.stream.Stream.*;

/**
 * Defines a relation and the operation that can be done with one or more
 * relations
 *
 * @author Dumitrescu Theodor A.
 */
public class Relation {

    private String name;
    private Header header;
    private Content content;

    public Relation(String name, Header header, Content content) {
        this.name = name;
        this.header = requireNonNull(header, "The header can't be null");
        this.content = requireNonNull(content, "The content can't be null");
    }

    public List<List<String>> getRows(String... attributes) {
        return content.getColumns(header.getAttributesIndex(attributes))
                .collect(toList());
    }

    public Set<List<String>> getRowsAsSet(String... attributes) {
        return content.getColumns(header.getAttributesIndex(attributes))
                .collect(toSet());
    }

    //TODO: readOnly method
    //TOOD: load and store functions
    public Relation selection(RecordFilter filter) {
        Content newC = new Content();

        this.content.stream()
                .map(Utilities::cast)
                .filter(filter)
                .map(Utilities::toString)
                .forEach(newC::add);

        return new Relation(name, header.clone(), newC);
    }

    public Relation product(Relation other) throws RelationalAlgebraException {

        if (header.sharedAttributes(other.header) != 0) {
            RelationalAlgebraException.throwError("Unable to perform product on relations with colliding attributes");
        }
        final List<List<String>> content = new ArrayList<>(this.content.size());

        this.content.forEach(i -> other.content.forEach(j -> 
                            content.add(
                                    concat(i.stream(), j.stream()).collect(toList()))
        ));
        
        return new Relation("", header.sum(other.header), new Content(content));
    }
    
    

}
