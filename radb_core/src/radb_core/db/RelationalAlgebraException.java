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

/**
 * Represent an Exception that is rise when there is an error
 * during an relational algebra operation
 * @author Dumitrescu Theodor A.
 */
public class RelationalAlgebraException extends Exception{

    public RelationalAlgebraException() {
    }
    
    public RelationalAlgebraException(String message) {
        super(message);
    }
    
    public RelationalAlgebraException(String message, Throwable cause) {
        super(message, cause);
    }
    
    public static final void throwError(String message) throws RelationalAlgebraException {
        throw new RelationalAlgebraException(message);
    }
}
