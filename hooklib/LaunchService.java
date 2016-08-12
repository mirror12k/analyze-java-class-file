
package hooklib;

import java.util.Arrays;
import java.lang.reflect.Method;
import java.net.URLClassLoader;

import hooklib.HookService;

public class LaunchService {
	public static String mainTargetClass = null;

	public static void main(String[] args) throws Exception {
		if (args.length == 0) {
			System.out.println("main class required");
		} else {
			String[] mainArgs = Arrays.copyOfRange(args, 1, args.length);

			Class[] classArgs = new Class[1];
			classArgs[0] = String[].class;
			Method mainMethod = hooklib.LaunchService.class.getClassLoader().loadClass(args[0]).getMethod("main", classArgs);

			Object[] invokeArgs = new Object[1];
			invokeArgs[0] = mainArgs;

			hooklib.HookService.startConsole();
			mainMethod.invoke(null, invokeArgs);
		}
	}
}

