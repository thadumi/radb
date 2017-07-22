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
package radb_core.util;

import java.util.Optional;
import java.util.function.Consumer;

/**
 *
 * @author thadumi
 */
class OptionalConsumer2<T> implements Consumer<Optional<T>> {

    private final Consumer<T> c;
    private final Command r;

    private OptionalConsumer2(Consumer<T> c, Command r) {
        this.c = c;
        this.r = r;
    }

    public static <T> OptionalConsumer2<T> of(Consumer<T> c, Command r) {
        return new OptionalConsumer2(c, r);
    }

    @Override
    public void accept(Optional<T> t) {
        if (t.isPresent()) {
            c.accept(t.get());
        } else {
            r.execut();
        }
    }
    
}
