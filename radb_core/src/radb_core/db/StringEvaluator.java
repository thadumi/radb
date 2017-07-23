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

import java.util.Calendar;
import java.util.Optional;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import radb_core.util.OptionalConsumer;

/**
 *
 * @author Dumitrescu Theodor A.
 */
final class StringEvaluator {
    private StringEvaluator() {
        throw new AssertionError();
    }
    
    public static boolean isInt(String s) {
        return s.matches("^[\\+\\-]{0,1}[0-9]+$");
    }
    
    public static boolean isReal(String s) {
        return s.matches("^[\\+\\-]{0,1}[0-9]+(\\.([0-9])+)?$");
    }
    
    public static boolean isDate(String s) {
        return s.matches("^([0-9]{1,4})(\\\\|-|/)([0-9]{1,2})(\\\\|-|/)([0-9]{1,2})$");
    }
    
    
    public static OptionalConsumer getInt(String s) {
        Integer i = null;
        
        if(isInt(s)) i = Integer.parseInt(s);
        
        return optionalOf(i);
    }
    
    public static OptionalConsumer getReal(String s) {
        Double d = null;
        
        if(isInt(s)) d = Double.parseDouble(s);
        
        return optionalOf(s);
    }
    
    public static OptionalConsumer getDate(String s) {
        Calendar c = null;
        
        Pattern pattern = Pattern.compile("^([0-9]{1,4})(\\\\|-|/)([0-9]{1,2})(\\\\|-|/)([0-9]{1,2})$");
        Matcher matcher = pattern.matcher(s);
        
        if (matcher.matches()) {
            c = Calendar.getInstance();
            
            int year = Integer.parseInt(matcher.group(1));
            int  mounth = Integer.parseInt(matcher.group(3)) - 1; //mounths start from 0 to 11
            int day = Integer.parseInt(matcher.group(5));
            
            c.set(Calendar.YEAR, year);
            c.set(Calendar.MONTH, mounth);
            c.set(Calendar.DAY_OF_MONTH, day);
            
        }
        
        //return OptionalConsumer.of(Optional.ofNullable(c));
        return optionalOf(c);
    }
    
    
    
    public static OptionalConsumer<?> cast(String s) {
        /*if(isInt(s)) return Integer.parseInt(s);
        
        if(isFloat(s)) return Double.parseDouble(s);
        
        if(isDate(s)) return getDate(s);
        
        return s;
        */
        class CastManager {
            private OptionalConsumer<?> oc;
            private final String s;
            
            public CastManager(final String s) {
                this.s = s;
            }
            
            private void performCast() {
                oc = getInt(s);
                oc.ifNotPresent(() -> {
                    oc = getReal(s);
                    oc.ifNotPresent(() -> { oc = getDate(s);});
                });
            }
            
            public OptionalConsumer<?> cast() {
                performCast();
                return oc;
            }
        }
        
        return new CastManager(s).cast();
        
    }
    
    
    private static <T> OptionalConsumer<T> optionalOf(T v) {
        return OptionalConsumer.of(Optional.ofNullable(v));
    }
    
}