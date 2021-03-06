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
import java.util.List;
import java.util.Objects;
//import static java.util.Objects.*;
import java.util.Set;
import java.util.function.Predicate;
import static java.util.stream.Collectors.*;
import static java.util.stream.IntStream.*;
import java.util.stream.Stream;
import static java.util.stream.Stream.*;

import static radb_core.util.Collections.*;
import static radb_core.util.Checker.*;

/**
 * Defines a relation and the operation that can be done with one or more
 * relations.
 * @author Dumitrescu Theodor A.
 */
public class Relation implements Cloneable {
    
    private String name; //name of the Relation
    private Header header; //header of the Relation
    private Content content; //content of the Relation

    /**
     * Relation constructor
     * @param name name of the Relation (used for storage operations)
     * @param header relation's header, it can't be null and can't be changed, 
     * @param content relation's content
     */
    Relation(String name, Header header, Content content) {
        this.name = Objects.isNull(name) ? "unnamed" : name;
        this.header = requireNonNull(header, "The header can't be null");
        this.content = requireNonNull(content, "The content can't be null");
    }
    
    /**
     * 
     * @param header
     * @param content 
     */
    public Relation(Header header, Content content) {
        this(null, header, content);
    }
    
    
    public static Relation of(String name, Header header, Content content) {
        return new Relation(name, header, content);
    }
    
    public static Relation of(Header header, Content content) {
        return of(null, header, content);
    }
    
    public static Relation of(String name, 
            List<String> headerAttributes,
            List<List<String>> records) {
        
        return new Relation(name, 
                            Header.of(headerAttributes), 
                            Content.of(records));
    }
    
    public Stream<List<String>> toRecords() {
        return content.clone().stream();
    }
    
    public List<List<String>> toRecordsAsList() {
        return content.clone().stream().collect(toList());
    }
    
    public Set<List<String>> toRecordsAsSet() {
        return content.stream().collect(toSet());
    }
    
    
    //TODO: readOnly method
    //TOOD: load and store functions
    
    /**
     * Apply the selection operation of the relation algebra to this relation 
     * @param filter  must be a valid boolean expression that define the records needed
     * @return a new relation that contains the resul
     */
    public Relation selection(RecordFilter filter) {
        Content newC = Content.emptyContent();

        this.content.stream()
                .map(Caster::cast) //cast each string value of the record in an aproprieted type
                .filter(filter) //applay the filter to the records
                .map(Caster::toString) //recast the records back into a record of strings
                .forEach(newC::add); //store the records into a new collection

        return of(name, header.clone(), newC);
    }

    /**
     * Perform a Cartesian Product between this relation and onther
     * @param other the second operator for the product operation
     * @return a new relation that contain the result of the operation
     * @throws RelationalAlgebraException if can't perform the product
     */
    public Relation product(Relation other) throws RelationalAlgebraException {

        if (header.sharedAttributes(other.header) != 0) { //to perform a Cartesian Product the relations must have different attributes
            RelationalAlgebraException.throwError("Unable to perform product on relations with colliding attributes");
        }
        
        final List<List<String>> content = new ArrayList<>(this.content.size());

        this.content.forEach(i -> other.content.forEach(j
                -> content.add(
                        concat(i.stream(), j.stream()).collect(toList()))
        ));

        return of(header.sum(other.header), Content.of(content));
    }
    
    /**
     * Create a projection of this relation, i.e. will create a new relation
     * that contains only some attributes
     * @param attributes attributes to add into the new relation
     * @return a new relation that contain the result
     * @throws RelationalAlgebraException may throw an error if the attributes list given 
     *                                    contains one or more attributes that don't belong 
     *                                    to this relation
     */
    public Relation projection(List<String> attributes) throws RelationalAlgebraException {
        if (attributes.isEmpty()) {
            return null;
        }

        List<Integer> ids = header.getAttributesIndex(attributes);

        if (ids.isEmpty() || ids.size() != attributes.size()) {
            RelationalAlgebraException.throwError("Invalid attributes for projection");
        }

        Header newHeader = Header.of(ids.stream().map(i -> header.getAttributes().get(i)).collect(toList()));

        Content newContent = Content.emptyContent();
        content.stream()
                .map(row
                        -> ids.stream().map(i -> row.get(i)).collect(toList()))
                .forEach(newContent::add);
        
        return of(newHeader, newContent);
    }
    
    /**
     *  Intersection operation. The result will contain items present in both operands.
     * @param other the second operand
     * @return a new realtion that contains the result
     * @throws RelationalAlgebraException if the headers are differents
     */
    public Relation intersection(Relation other) throws RelationalAlgebraException {
        other = rearrange(other);

        if (!header.equals(other.header)) {
            RelationalAlgebraException.throwError("Unable to perform intersection on relations with different attributes");
        }

        Header newHeader = header.clone();
        Content newContent = content.intersection(other.content);

        return of(newHeader, newContent);
    }
    
    /**
     * Performs the difference operation between this relation and seconds relation.
     * The result will contain items present in first
     * operand but not in second one.
     * @param other the second relation 
     * @return a new relation that contains the result
     * @throws RelationalAlgebraException if the two relations have different headers
     */
    public Relation difference(Relation other) throws RelationalAlgebraException {
        other = rearrange(other);

        if (!header.equals(other.header)) {
            RelationalAlgebraException.throwError("Unable to perform difference on relations with different attributes");
        }

        Header newheader = header.clone();
        Content newContent = content.difference(other.content);

        return of(newheader, newContent);
    }

    /**
     * The division is a binary operation that is written as R ÷ S. The
     * result consists of the restrictions of tuples in R to the
     * attribute names unique to R, i.e., in the header of R but not in the
     * header of S, for which it holds that all their combinations with tuples
     * in S are present in R.
     * @param other the second relation 
     * @return a new relation that contains the result
     * @throws RelationalAlgebraException 
     */
    public Relation division(Relation other) throws RelationalAlgebraException {
        //attributes from this relation and that arn't also in the second relation's header
        List<String> diffAttributes = header.difference(other.header).getAttributes(); 
        Relation projectionOfDiffAtt = projection(diffAttributes);

        Relation tmp = projectionOfDiffAtt.product(other);

        return projectionOfDiffAtt.difference(tmp.difference(this).projection(diffAttributes));
    }
    
    /**
     * Perform an union operation. The result will contain items present in first
     * and second operands.
     * @param other the second operand
     * @return a new relation that represents the result
     * @throws RelationalAlgebraException if the headers are different. 
     *                                    It's possible to use projection and rename
     *                                   operations to make headers match
     */
    public Relation union(Relation other) throws RelationalAlgebraException {
        other = rearrange(other);

        if (!header.equals(other.header)) {
            RelationalAlgebraException.throwError("Unable to perform difference on relations with different attributes");
        }

        return of(header.clone(), content.union(other.content));
    }
    
    public Relation join(Relation other, RecordFilter filter) throws RelationalAlgebraException {
        if (Objects.nonNull(filter)) {
            return product(other).selection(filter);
        }

        List<String> sharedAttributes = header.sharedAttributesAsList(other.header);

        List<String> newHeader = header.getAttributes();
        other.header.getAttributes().stream()
                .filter(att -> !sharedAttributes.contains(att))
                .forEach(newHeader::add);

        List<Integer> thisSharedId = getAttributesIndex(sharedAttributes);
        List<Integer> otherSharedId = other.getAttributesIndex(sharedAttributes);

        List<Integer> otherNotSharedId = range(0, other.numberOfColumns()).boxed()
                                            .filter(i -> !otherSharedId.contains(i))
                                            .collect(toList());

        List<List<String>> newContent = content.stream()
                .map(i -> other.content.stream()
                        .filter(j -> 
                                range(0,sharedAttributes.size()).boxed()
                                    .map(k -> i.get(thisSharedId.get(k)).equals(j.get(otherSharedId.get(k))))
                                    .reduce(Boolean.TRUE, (r, e) -> r && e)
                        )
                        .map(j
                                -> otherNotSharedId.stream().map(l -> j.get(l)).collect(toList()))
                        .collect(toList()))
                .flatMap(List::stream)
                .collect(toList());

        return of(Header.of(newHeader), Content.of(newContent));
    }
    
    
    public Relation outerLeft(Relation other) {
        List<String> sharedAttributes = header.sharedAttributesAsList(other.header);
        
        List<String> newHeaderAtt = new ArrayList<>(header.getAttributes());
        
        other.header.attributes()
                    .filter(attribute -> !sharedAttributes.contains(attribute))
                    .forEach(newHeaderAtt::add);
        
        Header newHeader = Header.of(newHeaderAtt);
        
        List<Integer> thisSharedId  = getAttributesIndex(sharedAttributes);
        List<Integer> otherSharedId = other.getAttributesIndex(sharedAttributes);
        
        List<Integer> otherNotSharedId = range(0, other.numberOfColumns()).boxed()
                                    .filter(i -> !otherSharedId.contains(i))
                                    .collect(toList());
        
        List<List<String>> newContent = content.stream()   //foreach thisRecord in content
                .map(i -> other.content.stream()           // foreach otherRecord in other.content
                        .map(j -> 
                            range(0,sharedAttributes.size()).boxed() //  foreach atrribute in sharedAttributes
                                .map(k -> i.get(thisSharedId.get(k)).equals(j.get(otherSharedId.get(k)))) //  check if thisRecord[attribute] == otherRecord[attribute]
                                .reduce(Boolean.TRUE, (r, e) -> r && e)  //  if
                                    ?   otherNotSharedId.stream().map(l -> j.get(l)) // all values are equal then create a list with the sharedAttributes' values of the otherRecord
                                    :   otherNotSharedId.stream().map(l -> Content.EMPTY)) // otherwaise create a list of empty field foreach shared attribute
                        .map( j -> concat(i.stream(), j).collect(toList())) //then concatenate thisRecord with the list created
                        .collect(toList())) // and save all the list in a new list as box
                .flatMap(List::stream) //take out all the list form each box
                .collect(toList()); // save all the list in a new list that will contain all the list
        return of(newHeader, Content.of(newContent));
    }
    
    public Relation outerRight(Relation other) {
        return other.outerLeft(this);
    }
    
    public Relation outer(Relation other) throws RelationalAlgebraException {
        return outerRight(other).union(outerLeft(other));
    }
    
    public Relation leftThetaJoin(Relation other, RecordFilter filter, boolean swap) {
        Header newHeader = !swap ? header.sum(other.header) : other.header.sum(header);
        
        Content newContet = Content.of(
            content.stream()
                .map(i -> other.content.stream()
                        .map(j -> 
                                filter.test(Caster.cast( !swap ? concat(i.stream(), j.stream()) : concat(i.stream(), j.stream())))
                                    ? (!swap ? concat(i.stream(), j.stream()) : concat(i.stream(), j.stream())).collect(toList())
                                    : (!swap ? concat(i.stream(), range(0, j.size()).mapToObj(k -> Content.EMPTY))
                                            : concat(range(0, j.size()).mapToObj(k -> Content.EMPTY), i.stream())).collect(toList()))  
                        .collect(toList()))
                .flatMap(List::stream)
                .collect(toList())
        );
        
        return of(newHeader, newContet);
    }
    
    public Relation leftThetaJoin(Relation other, RecordFilter filter) {
        return leftThetaJoin(other, filter, false);
    }
    
    public Relation rightThetaJoint(Relation other, RecordFilter filter) {
        return other.leftThetaJoin(this, filter, true);
    }
    
    public Relation fullThetaJoin(Relation other, RecordFilter filter) throws RelationalAlgebraException {
        return leftThetaJoin(other, filter).union(rightThetaJoint(other, filter));
    }
    
    //TOOD: update, insert, delete
    
    //relation.operator().sum(other).sum(other).valuate();
    
    
    /**
     * Returns a list with numeric index corresponding to field's name
     *
     * @param attributes
     * @return
     */
   public List<Integer> getAttributesIndex(List<String> attributes) {
        return header.getAttributesIndex(attributes);
    }

    public int getAttributeIndex(String attribute) {
        List<Integer> index = header.getAttributesIndex(attribute);

        return index.isEmpty() ? -1 : index.get(0);
    }

    private Relation rearrange(Relation other) {
        long sharedAttributes = header.sharedAttributes(other.header);

        if (sharedAttributes == header.getAttributes().size() && sharedAttributes == other.header.getAttributes().size()) {
            try {
                return other.projection(header.getAttributes());
            } catch (RelationalAlgebraException ex) {
                return null;
            }
        } else {
            return null;
        }
    }

    public int numberOfColumns() {
        return (int) header.size();
    }

    @Override
    protected Relation clone() {
        return of(name, header.clone(), content.clone());
    }

    @Override
    public String toString() {
        return "----------Table" + (name == null || name.isEmpty() ? "unamed" : name) + "----------\n"  
               + header.toString() + "\n" 
               + content.toString();
    }
    
    static final class Caster {
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

}
