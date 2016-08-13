
package hooklib;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;



public class HookService {
	private static ArrayList<HookService.GeneralValue> argstack = new ArrayList<HookService.GeneralValue>();

	private static HashMap<String, HookService.HookBreakpoint> callBreakpoints = new HashMap<String, HookService.HookBreakpoint>();
	private static HashMap<String, HookService.HookBreakpoint> callExactBreakpoints = new HashMap<String, HookService.HookBreakpoint>();


	public static String stringArgs() {
		int i = 0;
		String result = "";
		for (GeneralValue arg : HookService.argstack) {
			if (i != 0) {
				result += ", ";
			}
			result += "arg" + Integer.toString(i) + ": " + arg;
			i++;
		}
		return result;
	}
	public static String stringReturn() {
		if (argstack.size() == 0) {
			return "void";
		} else {
			return "" + argstack.get(0);
		}
	}

	public static void traceDynamicMethodCall(String methodname, Object thisObj) {
		System.out.println("[entr] " + methodname + " : (this: " + thisObj.getClass().getName() + "#" + Integer.toHexString(thisObj.hashCode()) +
				", "+ stringArgs() + ")");

		ArrayList<HookService.GeneralValue> oldargstack = argstack;
		argstack = new ArrayList<HookService.GeneralValue>();

		if (callBreakpoints.get(methodname.substring(0, methodname.indexOf(" ("))) != null) {
			startBreakpoint(new HookBreakpointInfo(methodname, thisObj, oldargstack, callBreakpoints.get(methodname.substring(0, methodname.indexOf(" (")))));
		} else if (callExactBreakpoints.get(methodname) != null) {
			startBreakpoint(new HookBreakpointInfo(methodname, thisObj, oldargstack, callExactBreakpoints.get(methodname)));
		}
	}

	public static void traceStaticMethodCall(String methodname) {
		System.out.println("[entr] " + methodname + " : (" + stringArgs() + ")");

		ArrayList<HookService.GeneralValue> oldargstack = argstack;
		argstack = new ArrayList<HookService.GeneralValue>();

		if (callBreakpoints.get(methodname.substring(0, methodname.indexOf(" ("))) != null) {
			startBreakpoint(new HookBreakpointInfo(methodname, null, oldargstack, callBreakpoints.get(methodname.substring(0, methodname.indexOf(" (")))));
		} else if (callExactBreakpoints.get(methodname) != null) {
			startBreakpoint(new HookBreakpointInfo(methodname, null, oldargstack, callExactBreakpoints.get(methodname)));
		}
	}

	public static void traceMethodReturn(String methodname) {
		System.out.println("[return] " + methodname + " : " + stringReturn());
		argstack = new ArrayList<HookService.GeneralValue>();
	}



	public static void startBreakpoint(HookBreakpointInfo info) {
		System.out.println("\nhooklib breakpoint at " + info.methodname);
		startConsole(info);
	}

	public static void startConsole(HookBreakpointInfo info) {

		Scanner input = new Scanner(System.in);

		Boolean readingCommands = true;
		while (readingCommands) {
			System.out.print("> ");
			String line = input.nextLine();

			try {
				if (line.equals("c")) {
					readingCommands = false;
					System.out.println("continuing");

				} else if (line.equals("q") || line.equals("exit")) {
					readingCommands = false;
					System.out.println("exiting application");
					System.exit(1);

				} else if (line.equals("st")) {
					System.out.println("stacktrace:");
					for (StackTraceElement el : Thread.currentThread().getStackTrace()) {
						System.out.println("\t" +el);
					}

				} else if (line.startsWith("b ")) {
					String breakTarget = line.substring("b ".length());
					if (breakTarget.indexOf(" (") == -1) {
						callBreakpoints.put(breakTarget, new HookBreakpoint());
					} else {
						callExactBreakpoints.put(breakTarget, new HookBreakpoint());
					}
					System.out.println("breakpoint created for [" + breakTarget + "]");

				} else if (line.startsWith("br ")) {
					String breakTarget = line.substring("br ".length());
					if (breakTarget.indexOf(" (") == -1) {
						callBreakpoints.remove(breakTarget);
					} else {
						callExactBreakpoints.remove(breakTarget);
					}
					System.out.println("breakpoint removed for [" + breakTarget + "]");

				} else if (line.equals("l b")) {
					System.out.println("current breakpoints:");
					for (String key : callBreakpoints.keySet()) {
						System.out.println("\t"+key);
					}
					for (String key : callExactBreakpoints.keySet()) {
						System.out.println("\t"+key);
					}

				} else if (line.startsWith("p ")) {
					String argument = line.substring("p ".length());
					if (argument.startsWith("this")) {
						argument = argument.substring("this".length());
						System.out.println("\tthis = " + info.thisarg);
					} else if (argument.startsWith("arg")) {
						argument = argument.substring("arg".length());
						int argnum = Integer.parseInt(argument);
						System.out.println("\targ"+argnum+" = " + info.argstack.get(argnum));
					} else {
						System.out.println("invalid argument for p: " + argument);
					}

				} else {
					System.out.println("unknown command");
				}
			} catch (Exception e) {
				System.out.println("exception occured handling input: " + e);
				e.printStackTrace();
			}
		}
	}



	public static void main(String[] args) {
		pushArg(15);
		pushArg("hello world!");
		pushArg(0.025);

		System.out.println(stringArgs());
	}


	public static void pushArg(boolean arg) {
		argstack.add(new HookService.GeneralValue(arg));
	}
	public static void pushArg(char arg) {
		argstack.add(new HookService.GeneralValue(arg));
	}
	public static void pushArg(byte arg) {
		argstack.add(new HookService.GeneralValue(arg));
	}
	public static void pushArg(short arg) {
		argstack.add(new HookService.GeneralValue(arg));
	}
	public static void pushArg(int arg) {
		argstack.add(new HookService.GeneralValue(arg));
	}
	public static void pushArg(long arg) {
		argstack.add(new HookService.GeneralValue(arg));
	}
	public static void pushArg(float arg) {
		argstack.add(new HookService.GeneralValue(arg));
	}
	public static void pushArg(double arg) {
		argstack.add(new HookService.GeneralValue(arg));
	}
	public static void pushArg(java.lang.Object arg) {
		argstack.add(new HookService.GeneralValue(arg));
	}

	public static enum GeneralValueType {
		VALUE_TYPE_BOOLEAN,
		VALUE_TYPE_CHAR,
		VALUE_TYPE_BYTE,
		VALUE_TYPE_SHORT,
		VALUE_TYPE_INT,
		VALUE_TYPE_LONG,
		VALUE_TYPE_FLOAT,
		VALUE_TYPE_DOUBLE,
		VALUE_TYPE_OBJECT,
	}

	public static class GeneralValue {
		public HookService.GeneralValueType type;

		public boolean val_boolean;
		public char val_char;
		public byte val_byte;
		public short val_short;
		public int val_int;
		public long val_long;
		public float val_float;
		public double val_double;
		public Object val_object;

		public GeneralValue(boolean val) {
			this.type = GeneralValueType.VALUE_TYPE_BOOLEAN;
			this.val_boolean = val;
		}
		public GeneralValue(char val) {
			this.type = GeneralValueType.VALUE_TYPE_CHAR;
			this.val_char = val;
		}
		public GeneralValue(byte val) {
			this.type = GeneralValueType.VALUE_TYPE_BYTE;
			this.val_byte = val;
		}
		public GeneralValue(short val) {
			this.type = GeneralValueType.VALUE_TYPE_SHORT;
			this.val_short = val;
		}
		public GeneralValue(int val) {
			this.type = GeneralValueType.VALUE_TYPE_INT;
			this.val_int = val;
		}
		public GeneralValue(long val) {
			this.type = GeneralValueType.VALUE_TYPE_LONG;
			this.val_long = val;
		}
		public GeneralValue(float val) {
			this.type = GeneralValueType.VALUE_TYPE_FLOAT;
			this.val_float = val;
		}
		public GeneralValue(double val) {
			this.type = GeneralValueType.VALUE_TYPE_DOUBLE;
			this.val_double = val;
		}
		public GeneralValue(Object val) {
			this.type = GeneralValueType.VALUE_TYPE_OBJECT;
			this.val_object = val;
		}

		public String toString() {
			switch (this.type) {
			case VALUE_TYPE_BOOLEAN:
				return java.lang.Boolean.toString(this.val_boolean);
			case VALUE_TYPE_CHAR:
				return java.lang.Character.toString(this.val_char);
			case VALUE_TYPE_BYTE:
				return java.lang.Byte.toString(this.val_byte);
			case VALUE_TYPE_SHORT:
				return java.lang.Short.toString(this.val_short);
			case VALUE_TYPE_INT:
				return java.lang.Integer.toString(this.val_int);
			case VALUE_TYPE_LONG:
				return java.lang.Long.toString(this.val_long);
			case VALUE_TYPE_FLOAT:
				return java.lang.Float.toString(this.val_float);
			case VALUE_TYPE_DOUBLE:
				return java.lang.Double.toString(this.val_double);
			case VALUE_TYPE_OBJECT:
				if (this.val_object == null) {
					return "null";
				} else {
					return this.val_object.getClass().getName() + "#" + Integer.toHexString(this.val_object.hashCode());
					// return this.val_object.toString();
				}
			default:
				return "**UNKNOWN**";
			}
		}
	}


	public static class HookBreakpoint {

	}

	public static class HookBreakpointInfo {
		public String methodname;

		public Object thisarg;
		public ArrayList<HookService.GeneralValue> argstack;
		public HookBreakpoint breakpoint;

		public HookBreakpointInfo(String methodname, Object thisarg, ArrayList<HookService.GeneralValue> argstack, HookBreakpoint breakpoint) {
			this.methodname = methodname;
			this.thisarg = thisarg;
			this.argstack = argstack;
			this.breakpoint = breakpoint;
		}
	}
}
