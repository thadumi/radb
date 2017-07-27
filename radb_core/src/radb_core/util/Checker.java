/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package radb_core.util;

import java.util.Objects;
import java.util.function.Predicate;

/**
 *
 * @author thadumi
 */
public final class Checker {
    private Checker(){}
    
    public static <T> T requireNonNull(T t, String mess) {
        return Objects.requireNonNull(t, mess);
    }
    
    public static <T> T throwIf(T t, Predicate<T> checker, String msg) {
        if(checker.test(t))
            throw new IllegalArgumentException(msg);
        
        return t;
    }
    
    public static <T> T throwIf(T t, Predicate<T> checker) {
        return throwIf(t, checker, "");
    }
}
    
