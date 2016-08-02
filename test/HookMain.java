
public class HookMain {
	public static void main__hooked(String[] args) {}
	public static void main(String[] args) {
		System.out.println("in main hook!");
		HookMain.main__hooked(args);
		System.out.println("left main");
	}
}
