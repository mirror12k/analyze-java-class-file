
import java.util.ArrayList;

public class HookService {
	private static ArrayList<HookService.GeneralValue> argstack;

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
				return this.val_object.toString();
			default:
				return "**UNKNOWN**";
			}
		}
	}
}
