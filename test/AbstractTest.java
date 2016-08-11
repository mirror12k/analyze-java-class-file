
public class AbstractTest {
	int val = 0;

	public void setVal(int nval) {
		this.val = nval;
	}
	public int getVal() {
		return this.val;
	}

	public static void main(String[] args) {
		AbstractTest obj = new AbstractTest();
		obj.setVal(15);
		System.out.println(obj.getVal());
	}
}
