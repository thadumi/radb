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

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;
import static java.util.stream.Collectors.*;
import java.util.stream.Stream;


import static radb_core.util.Checker.*;

/**
 * This class defines the header of a Relation
 *
 * @author Dumitrescu Theodor A.
 */
public class Header implements Cloneable {

    /**
     * {
     * (nome, str) (eta, int) }
     */
    //List<Pair<String, String>> header;

    private final List<String> attributes;

    Header(Collection<String> attributes) throws IllegalArgumentException {
        this.attributes = new ArrayList<>(attributes);
        
        if (!this.attributes.stream().allMatch(Header::checkName)) {
            throw new IllegalArgumentException("There is some attributes with a not valid attribute name");
        }
    }
    
    public static Header of(List<String> attributes) {
        requireNonNull(attributes, "");
        throwIf(attributes, Collection::isEmpty);
        
        return new Header(new LinkedHashSet<>(attributes));
    }
    
    public static Header of(String ... attributes) {
        throwIf(attributes, arg -> arg.length < 1);
        
        return Header.of(Arrays.asList(attributes));
    }
    
    public static Header of(String attributes) {
        requireNonNull(attributes, "attributes can't be null");
        throwIf(attributes, arg -> arg.length() < 1);
        
        return Header.of(attributes.split(", "));
    }

    /**
     * Change the name of an attribute
     *
     * @param _old name of the attribute
     * @param _new name to be set
     * @return true if the change is done correctly
     */
    public boolean rename(String _old, String _new) {
        int index = attributes.indexOf(_old);
        
        if(index < 0) return false;
        
        attributes.set(index, _new);
        return true;
    }

    /**
     * Count how many attributes this header as in common with a given one.
     *
     * @param other the other header to compare.
     * @return
     */
    public long sharedAttributes(Header other) {
        return sharedAttributesAsList(other).size();
    }
    
    public List<String> sharedAttributesAsList(Header other) {
        return attributes.stream()
                .filter(att -> other.getAttributes().contains(att))
                .collect(toList());
    }
    
    public Stream<String> attributes() {
        return getAttributes().stream();
    }

    public List<String> getAttributes() {
        return Collections.unmodifiableList(attributes);
    }

    public long size() { return attributes.size(); }
    
    /**
     * Returns a list with numeric index corresponding to field's name
     * @param attributes
     * @return 
     */
    public List<Integer> getAttributesIndex(String... attributes) {
        return getAttributesIndex(Arrays.asList(attributes));
    }

    public List<Integer> getAttributesIndex(List<String> attributes) {
        return this.attributes.stream()
                .filter(att -> attributes.contains(att))
                .map(att -> this.attributes.indexOf(att))
                .collect(toList());
    }

    public Header sum(Header other) {
        Set<String> newAtt = new LinkedHashSet<>(attributes);
        newAtt.addAll(other.attributes);
        
        return new Header(newAtt.stream().collect(toList()));
    }
    
    public Header difference(Header other) {
        List<String> newAtt = new ArrayList<>(attributes);
        
        newAtt.removeAll(other.attributes);
        
        return new Header(newAtt);
    }
    
    
    @Override
    public boolean equals(Object obj) {
        if (obj instanceof Header) {
            return this == obj || attributes.equals(((Header) obj).getAttributes());
        } else {
            return false;
        }
    }

    @Override
    public int hashCode() {
        int hash = 0x7;
        hash = 0x4f * hash + Objects.hashCode(this.attributes);
        return hash;
    }

    @Override
    public String toString() {
        return attributes.stream().collect(joining(", ", "", ""));
    }

    @Override
    protected Header clone() {
        return new Header(attributes);
    }

    private static boolean checkName(String att) {
        //TODO : add regex for the attribute name
        return true;
    }

}
