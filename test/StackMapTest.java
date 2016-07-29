
public class StackMapTest {

	public static void main(String[] args) {
		String data = "";
		try {
			for (int i = 0; i < 10; i++) {
				data += Integer.toString(i);
			}
			System.out.println("value: " + data);
		} catch (Exception e) {
			System.out.println("error occured!");
		}
	}
}
