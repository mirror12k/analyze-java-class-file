
public class PrintTest {
	public static void main(String[] args) {
		PrintTest.SomeClass obj = null;
		System.out.println("my obj: "+obj+","+args+","+5);
	}
	public static class SomeClass {
		SomeClass() {
		}
	}
}