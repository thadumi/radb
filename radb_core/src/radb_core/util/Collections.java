/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package radb_core.util;

import java.util.List;
import static java.util.Arrays.*;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
/**
 *
 * @author thadumi
 */
public final  class Collections {
    private Collections() {}
    
    /**
     * Convert an array of T into an list of T elements
     * @param <T> type of the object stored into the array
     * @param array array that will be convert into a list
     * @return a list that contains the elements of the array
     */
    public static <T> List<T> toList(T[] array) {
        return stream(array).collect(Collectors.toList());
    }
    
    public static List<Integer> toList(int[] array) {
        return IntStream.of(array).boxed().collect(Collectors.toList());
    }
}
