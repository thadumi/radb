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
package radb_core.util;

import java.util.Objects;
import java.util.function.Function;
import java.util.function.Predicate;

/**
 *
 * @author thadumi
 */
public final class Checker {

    private Checker() {
    }

    public static <T> T requireNonNull(T t, String mess) {
        return Objects.requireNonNull(t, mess);
    }
    
    
    public static void throwIf(boolean condition, String msg) {
        if(condition)
            throw new IllegalArgumentException(msg);
        
    }
    
    
    
    public static <T> T throwIf(T t, Predicate<T> checker, String msg) {
        throwIf(checker.test(t), msg);
        return t;
    }

    public static <T> T throwIf(T t, Predicate<T> checker) {
        return throwIf(t, checker, "");
    }
    

    
    public static <T> T throwIf(T t, Supplier<Boolean> checker, String msg) {
        throwIf(checker.get(), msg);
        return t;
    }

    public static <T> T throwIf(T t, Supplier<Boolean> checker) {
        return throwIf(t, checker, "");
    }
    
    public static void throwIf(Supplier<Boolean> checker, String msg) {
        throwIf(checker.get(), msg);
    }
    
    public static void thowIf(Supplier<Boolean> checker) {
        throwIf(checker, "");
    }
    
    public static class Thrower {
        boolean condition;
        //String msg;
        //Supplier<? extends Throwable> throwableMaker;
        
        public static Thrower If(boolean condition) {
            Thrower t = new Thrower();
            t.condition = condition;
            
            return t;
        }
        
        public <T extends Exception> void Throw(Function<String, T> excemptionMaker, String msg) throws T{
            if(Objects.isNull(excemptionMaker))
                return;
            
            if(condition)
                throw excemptionMaker.apply(msg);
        }
        
        public void Throw(Supplier<? extends Exception> excemptionMaker) throws Exception{
            if(Objects.isNull(excemptionMaker)) excemptionMaker = Exception::new;
        
            if(condition)
                throw excemptionMaker.get();
        }
       
    }
    
    public static Thrower If(boolean condition) {
        return Thrower.If(condition);
    }
}
