
public class LookupTest {
	public static void main(String[] args) {
		int val = 1500000;
		switch (val) {
		case 1337:
			System.out.println("val is 1337");
			break;
		case 4000000:
			System.out.println("val is 2000000+2000000");
			break;
		case 1500000:
			System.out.println("val is 150000015000001500000");
			break;
		case 1234567:
			System.out.println("val is 1234567?");
			break;
		}
	}
}
