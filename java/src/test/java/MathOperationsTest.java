import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class MathOperationsTest {
    @Test
    public void testAdd() {
        assertEquals(5, MathOperations.add(2, 3));
    }

    @Test
    public void testSubtract() {
        assertEquals(2, MathOperations.subtract(5, 3));
    }

//    @Test
//    public void testMultiply() {
//        assertEquals(6, MathOperations.multiply(2, 3));
//    }

    @Test
    public void testDivide() {
        assertEquals(3.0, MathOperations.divide(6, 2));
        Exception exception = assertThrows(ArithmeticException.class, () -> {
            MathOperations.divide(6, 0);
        });
        assertEquals("Cannot divide by zero", exception.getMessage());
    }
}