
public class ExceptionTest {
	public static void main(String[] args) throws RuntimeException {
		try {
			System.out.println("hello world!");
		} catch (RuntimeException e) {
			System.out.println("runtime exception occured");
		}
	}
}
