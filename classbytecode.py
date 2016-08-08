


import struct

import classfile
from java_code_tools import *




bytecode0ToAssembly = {
	0x00 : 'nop',
	0x01 : 'aconst_null',
	0x02 : 'iconst_m1',
	0x03 : 'iconst_0',
	0x04 : 'iconst_1',
	0x05 : 'iconst_2',
	0x06 : 'iconst_3',
	0x07 : 'iconst_4',
	0x08 : 'iconst_5',
	0x09 : 'lconst_0',
	0x0a : 'lconst_1',
	0x0b : 'fconst_0',
	0x0c : 'fconst_1',
	0x0d : 'fconst_2',
	0x0e : 'dconst_0',
	0x0f : 'dconst_1',
	0x1a : 'iload_0',
	0x1b : 'iload_1',
	0x1c : 'iload_2',
	0x1d : 'iload_3',
	0x1e : 'lload_0',
	0x1f : 'lload_1',
	0x20 : 'lload_2',
	0x21 : 'lload_3',
	0x22 : 'fload_0',
	0x23 : 'fload_1',
	0x24 : 'fload_2',
	0x25 : 'fload_3',
	0x26 : 'dload_0',
	0x27 : 'dload_1',
	0x28 : 'dload_2',
	0x29 : 'dload_3',
	0x2a : 'aload_0',
	0x2b : 'aload_1',
	0x2c : 'aload_2',
	0x2d : 'aload_3',
	0x2e : 'iaload',
	0x2f : 'laload',
	0x30 : 'faload',
	0x31 : 'daload',
	0x32 : 'aaload',
	0x33 : 'baload',
	0x34 : 'caload',
	0x35 : 'saload',
	0x3b : 'istore_0',
	0x3c : 'istore_1',
	0x3d : 'istore_2',
	0x3e : 'istore_3',
	0x3f : 'lstore_0',
	0x40 : 'lstore_1',
	0x41 : 'lstore_2',
	0x42 : 'lstore_3',
	0x43 : 'fstore_0',
	0x44 : 'fstore_1',
	0x45 : 'fstore_2',
	0x46 : 'fstore_3',
	0x47 : 'dstore_0',
	0x48 : 'dstore_1',
	0x49 : 'dstore_2',
	0x4a : 'dstore_3',
	0x4b : 'astore_0',
	0x4c : 'astore_1',
	0x4d : 'astore_2',
	0x4e : 'astore_3',
	0x4f : 'iastore',
	0x50 : 'lastore',
	0x51 : 'fastore',
	0x52 : 'dastore',
	0x53 : 'aastore',
	0x54 : 'bastore',
	0x55 : 'castore',
	0x56 : 'sastore',
	0x57 : 'pop',
	0x58 : 'pop2',
	0x59 : 'dup',
	0x5a : 'dup_x1',
	0x5b : 'dup_x2',
	0x5c : 'dup2',
	0x5d : 'dup2_x1',
	0x5e : 'dup2_x2',
	0x5f : 'swap',
	0x60 : 'iadd',
	0x61 : 'ladd',
	0x62 : 'fadd',
	0x63 : 'dadd',
	0x64 : 'isub',
	0x65 : 'lsub',
	0x66 : 'fsub',
	0x67 : 'dsub',
	0x68 : 'imul',
	0x69 : 'lmul',
	0x6a : 'fmul',
	0x6b : 'dmul',
	0x6c : 'idiv',
	0x6d : 'ldiv',
	0x6e : 'fdiv',
	0x6f : 'ddiv',
	0x70 : 'irem',
	0x71 : 'lrem',
	0x72 : 'frem',
	0x73 : 'drem',
	0x74 : 'ineg',
	0x75 : 'lneg',
	0x76 : 'fneg',
	0x77 : 'dneg',
	0x78 : 'ishl',
	0x79 : 'lshl',
	0x7a : 'ishr',
	0x7b : 'lshr',
	0x7c : 'iushr',
	0x7d : 'lushr',
	0x7e : 'iand',
	0x7f : 'land',
	0x80 : 'ior',
	0x81 : 'lor',
	0x82 : 'ixor',
	0x83 : 'lxor',
	0x85 : 'i2l',
	0x86 : 'i2f',
	0x87 : 'i2d',
	0x88 : 'l2i',
	0x89 : 'l2f',
	0x8a : 'l2d',
	0x8b : 'f2i',
	0x8c : 'f2l',
	0x8d : 'f2d',
	0x8e : 'd2i',
	0x8f : 'd2l',
	0x90 : 'd2f',
	0x91 : 'i2b',
	0x92 : 'i2c',
	0x93 : 'i2s',
	0x94 : 'lcmp',
	0x95 : 'fcmpl',
	0x96 : 'fcmpg',
	0x97 : 'dcmpl',
	0x98 : 'dcmpg',
	0xac : 'ireturn',
	0xad : 'lreturn',
	0xae : 'freturn',
	0xaf : 'dreturn',
	0xb0 : 'areturn',
	0xb1 : 'return',
	0xbe : 'arraylength',
	0xbf : 'athrow',
	0xc2 : 'monitorenter',
	0xc3 : 'monitorexit',
	0xca : 'breakpoint',
	0xfe : 'impdep1',
	0xff : 'impdep2',
}

bytecode1ToAssembly = {
	0x10 : 'bipush',
	0x12 : 'ldc',
	0x15 : 'iload',
	0x16 : 'lload',
	0x17 : 'fload',
	0x18 : 'dload',
	0x19 : 'aload',
	0x36 : 'istore',
	0x37 : 'lstore',
	0x38 : 'fstore',
	0x39 : 'dstore',
	0x3a : 'astore',
	0xa9 : 'ret',
	0xbc : 'newarray',
}

bytecode2ToAssembly = {
	0x11 : 'sipush',
	0x13 : 'ldc_w',
	0x14 : 'ldc2_w',
	0x84 : 'iinc',
	0x99 : 'ifeq',
	0x9a : 'ifne',
	0x9b : 'iflt',
	0x9c : 'ifge',
	0x9d : 'ifgt',
	0x9e : 'ifle',
	0x9f : 'if_icmpeq',
	0xa0 : 'if_icmpne',
	0xa1 : 'if_icmplt',
	0xa2 : 'if_icmpge',
	0xa3 : 'if_icmpgt',
	0xa4 : 'if_icmple',
	0xa5 : 'if_acmpeq',
	0xa6 : 'if_acmpne',
	0xa7 : 'goto',
	0xa8 : 'jsr',
	0xb2 : 'getstatic',
	0xb3 : 'putstatic',
	0xb4 : 'getfield',
	0xb5 : 'putfield',
	0xb6 : 'invokevirtual',
	0xb7 : 'invokespecial',
	0xb8 : 'invokestatic',
	0xbb : 'new',
	0xbd : 'anewarray',
	0xc0 : 'checkcast',
	0xc1 : 'instanceof',
	0xc6 : 'ifnull',
	0xc7 : 'ifnonnull',
}

bytecodeOtherToAssembly = {
	0xaa : 'tableswitch',
	0xab : 'lookupswitch',
	0xb9 : 'invokeinterface',
	0xba : 'invokedynamic',
	0xc4 : 'wide',
	0xc5 : 'multianewarray',
	0xc8 : 'goto_w',
	0xc9 : 'jsr_w',
}





assemblyToBytecode = {
	'aaload' : 0x32,
	'aastore' : 0x53,
	'aconst_null' : 0x01,
	'aload' : 0x19,
	'aload_0' : 0x2a,
	'aload_1' : 0x2b,
	'aload_2' : 0x2c,
	'aload_3' : 0x2d,
	'anewarray' : 0xbd,
	'areturn' : 0xb0,
	'arraylength' : 0xbe,
	'astore' : 0x3a,
	'astore_0' : 0x4b,
	'astore_1' : 0x4c,
	'astore_2' : 0x4d,
	'astore_3' : 0x4e,
	'athrow' : 0xbf,
	'baload' : 0x33,
	'bastore' : 0x54,
	'bipush' : 0x10,
	'breakpoint' : 0xca,
	'caload' : 0x34,
	'castore' : 0x55,
	'checkcast' : 0xc0,
	'd2f' : 0x90,
	'd2i' : 0x8e,
	'd2l' : 0x8f,
	'dadd' : 0x63,
	'daload' : 0x31,
	'dastore' : 0x52,
	'dcmpg' : 0x98,
	'dcmpl' : 0x97,
	'dconst_0' : 0x0e,
	'dconst_1' : 0x0f,
	'ddiv' : 0x6f,
	'dload' : 0x18,
	'dload_0' : 0x26,
	'dload_1' : 0x27,
	'dload_2' : 0x28,
	'dload_3' : 0x29,
	'dmul' : 0x6b,
	'dneg' : 0x77,
	'drem' : 0x73,
	'dreturn' : 0xaf,
	'dstore' : 0x39,
	'dstore_0' : 0x47,
	'dstore_1' : 0x48,
	'dstore_2' : 0x49,
	'dstore_3' : 0x4a,
	'dsub' : 0x67,
	'dup' : 0x59,
	'dup_x1' : 0x5a,
	'dup_x2' : 0x5b,
	'dup2' : 0x5c,
	'dup2_x1' : 0x5d,
	'dup2_x2' : 0x5e,
	'f2d' : 0x8d,
	'f2i' : 0x8b,
	'f2l' : 0x8c,
	'fadd' : 0x62,
	'faload' : 0x30,
	'fastore' : 0x51,
	'fcmpg' : 0x96,
	'fcmpl' : 0x95,
	'fconst_0' : 0x0b,
	'fconst_1' : 0x0c,
	'fconst_2' : 0x0d,
	'fdiv' : 0x6e,
	'fload' : 0x17,
	'fload_0' : 0x22,
	'fload_1' : 0x23,
	'fload_2' : 0x24,
	'fload_3' : 0x25,
	'fmul' : 0x6a,
	'fneg' : 0x76,
	'frem' : 0x72,
	'freturn' : 0xae,
	'fstore' : 0x38,
	'fstore_0' : 0x43,
	'fstore_1' : 0x44,
	'fstore_2' : 0x45,
	'fstore_3' : 0x46,
	'fsub' : 0x66,
	'getfield' : 0xb4,
	'getstatic' : 0xb2,
	'goto' : 0xa7,
	'goto_w' : 0xc8,
	'i2b' : 0x91,
	'i2c' : 0x92,
	'i2d' : 0x87,
	'i2f' : 0x86,
	'i2l' : 0x85,
	'i2s' : 0x93,
	'iadd' : 0x60,
	'iaload' : 0x2e,
	'iand' : 0x7e,
	'iastore' : 0x4f,
	'iconst_m1' : 0x02,
	'iconst_0' : 0x03,
	'iconst_1' : 0x04,
	'iconst_2' : 0x05,
	'iconst_3' : 0x06,
	'iconst_4' : 0x07,
	'iconst_5' : 0x08,
	'idiv' : 0x6c,
	'if_acmpeq' : 0xa5,
	'if_acmpne' : 0xa6,
	'if_icmpeq' : 0x9f,
	'if_icmpge' : 0xa2,
	'if_icmpgt' : 0xa3,
	'if_icmple' : 0xa4,
	'if_icmplt' : 0xa1,
	'if_icmpne' : 0xa0,
	'ifeq' : 0x99,
	'ifge' : 0x9c,
	'ifgt' : 0x9d,
	'ifle' : 0x9e,
	'iflt' : 0x9b,
	'ifne' : 0x9a,
	'ifnonnull' : 0xc7,
	'ifnull' : 0xc6,
	'iinc' : 0x84,
	'iload' : 0x15,
	'iload_0' : 0x1a,
	'iload_1' : 0x1b,
	'iload_2' : 0x1c,
	'iload_3' : 0x1d,
	'impdep1' : 0xfe,
	'impdep2' : 0xff,
	'imul' : 0x68,
	'ineg' : 0x74,
	'instanceof' : 0xc1,
	'invokedynamic' : 0xba,
	'invokeinterface' : 0xb9,
	'invokespecial' : 0xb7,
	'invokestatic' : 0xb8,
	'invokevirtual' : 0xb6,
	'ior' : 0x80,
	'irem' : 0x70,
	'ireturn' : 0xac,
	'ishl' : 0x78,
	'ishr' : 0x7a,
	'istore' : 0x36,
	'istore_0' : 0x3b,
	'istore_1' : 0x3c,
	'istore_2' : 0x3d,
	'istore_3' : 0x3e,
	'isub' : 0x64,
	'iushr' : 0x7c,
	'ixor' : 0x82,
	'jsr' : 0xa8,
	'jsr_w' : 0xc9,
	'l2d' : 0x8a,
	'l2f' : 0x89,
	'l2i' : 0x88,
	'ladd' : 0x61,
	'laload' : 0x2f,
	'land' : 0x7f,
	'lastore' : 0x50,
	'lcmp' : 0x94,
	'lconst_0' : 0x09,
	'lconst_1' : 0x0a,
	'ldc' : 0x12,
	'ldc_w' : 0x13,
	'ldc2_w' : 0x14,
	'ldiv' : 0x6d,
	'lload' : 0x16,
	'lload_0' : 0x1e,
	'lload_1' : 0x1f,
	'lload_2' : 0x20,
	'lload_3' : 0x21,
	'lmul' : 0x69,
	'lneg' : 0x75,
	'lookupswitch' : 0xab,
	'lor' : 0x81,
	'lrem' : 0x71,
	'lreturn' : 0xad,
	'lshl' : 0x79,
	'lshr' : 0x7b,
	'lstore' : 0x37,
	'lstore_0' : 0x3f,
	'lstore_1' : 0x40,
	'lstore_2' : 0x41,
	'lstore_3' : 0x42,
	'lsub' : 0x65,
	'lushr' : 0x7d,
	'lxor' : 0x83,
	'monitorenter' : 0xc2,
	'monitorexit' : 0xc3,
	'multianewarray' : 0xc5,
	'new' : 0xbb,
	'newarray' : 0xbc,
	'nop' : 0x00,
	'pop' : 0x57,
	'pop2' : 0x58,
	'putfield' : 0xb5,
	'putstatic' : 0xb3,
	'ret' : 0xa9,
	'return' : 0xb1,
	'saload' : 0x35,
	'sastore' : 0x56,
	'sipush' : 0x11,
	'swap' : 0x5f,
	'tableswitch' : 0xaa,
	'wide' : 0xc4,
}




assemblyToSizeTable = {
	'nop' : 1,
	'aconst_null' : 1,
	'iconst_m1' : 1,
	'iconst_0' : 1,
	'iconst_1' : 1,
	'iconst_2' : 1,
	'iconst_3' : 1,
	'iconst_4' : 1,
	'iconst_5' : 1,
	'lconst_0' : 1,
	'lconst_1' : 1,
	'fconst_0' : 1,
	'fconst_1' : 1,
	'fconst_2' : 1,
	'dconst_0' : 1,
	'dconst_1' : 1,
	'iload_0' : 1,
	'iload_1' : 1,
	'iload_2' : 1,
	'iload_3' : 1,
	'lload_0' : 1,
	'lload_1' : 1,
	'lload_2' : 1,
	'lload_3' : 1,
	'fload_0' : 1,
	'fload_1' : 1,
	'fload_2' : 1,
	'fload_3' : 1,
	'dload_0' : 1,
	'dload_1' : 1,
	'dload_2' : 1,
	'dload_3' : 1,
	'aload_0' : 1,
	'aload_1' : 1,
	'aload_2' : 1,
	'aload_3' : 1,
	'iaload' : 1,
	'laload' : 1,
	'faload' : 1,
	'daload' : 1,
	'aaload' : 1,
	'baload' : 1,
	'caload' : 1,
	'saload' : 1,
	'istore_0' : 1,
	'istore_1' : 1,
	'istore_2' : 1,
	'istore_3' : 1,
	'lstore_0' : 1,
	'lstore_1' : 1,
	'lstore_2' : 1,
	'lstore_3' : 1,
	'fstore_0' : 1,
	'fstore_1' : 1,
	'fstore_2' : 1,
	'fstore_3' : 1,
	'dstore_0' : 1,
	'dstore_1' : 1,
	'dstore_2' : 1,
	'dstore_3' : 1,
	'astore_0' : 1,
	'astore_1' : 1,
	'astore_2' : 1,
	'astore_3' : 1,
	'iastore' : 1,
	'lastore' : 1,
	'fastore' : 1,
	'dastore' : 1,
	'aastore' : 1,
	'bastore' : 1,
	'castore' : 1,
	'sastore' : 1,
	'pop' : 1,
	'pop2' : 1,
	'dup' : 1,
	'dup_x1' : 1,
	'dup_x2' : 1,
	'dup2' : 1,
	'dup2_x1' : 1,
	'dup2_x2' : 1,
	'swap' : 1,
	'iadd' : 1,
	'ladd' : 1,
	'fadd' : 1,
	'dadd' : 1,
	'isub' : 1,
	'lsub' : 1,
	'fsub' : 1,
	'dsub' : 1,
	'imul' : 1,
	'lmul' : 1,
	'fmul' : 1,
	'dmul' : 1,
	'idiv' : 1,
	'ldiv' : 1,
	'fdiv' : 1,
	'ddiv' : 1,
	'irem' : 1,
	'lrem' : 1,
	'frem' : 1,
	'drem' : 1,
	'ineg' : 1,
	'lneg' : 1,
	'fneg' : 1,
	'dneg' : 1,
	'ishl' : 1,
	'lshl' : 1,
	'ishr' : 1,
	'lshr' : 1,
	'iushr' : 1,
	'lushr' : 1,
	'iand' : 1,
	'land' : 1,
	'ior' : 1,
	'lor' : 1,
	'ixor' : 1,
	'lxor' : 1,
	'i2l' : 1,
	'i2f' : 1,
	'i2d' : 1,
	'l2i' : 1,
	'l2f' : 1,
	'l2d' : 1,
	'f2i' : 1,
	'f2l' : 1,
	'f2d' : 1,
	'd2i' : 1,
	'd2l' : 1,
	'd2f' : 1,
	'i2b' : 1,
	'i2c' : 1,
	'i2s' : 1,
	'lcmp' : 1,
	'fcmpl' : 1,
	'fcmpg' : 1,
	'dcmpl' : 1,
	'dcmpg' : 1,
	'ireturn' : 1,
	'lreturn' : 1,
	'freturn' : 1,
	'dreturn' : 1,
	'areturn' : 1,
	'return' : 1,
	'arraylength' : 1,
	'athrow' : 1,
	'monitorenter' : 1,
	'monitorexit' : 1,
	'breakpoint' : 1,
	'impdep1' : 1,
	'impdep2' : 1,


	'bipush' : 2,
	'ldc' : 2,
	'iload' : 2,
	'lload' : 2,
	'fload' : 2,
	'dload' : 2,
	'aload' : 2,
	'istore' : 2,
	'lstore' : 2,
	'fstore' : 2,
	'dstore' : 2,
	'astore' : 2,
	'ret' : 2,
	'newarray' : 2,



	'sipush' : 3,
	'ldc_w' : 3,
	'ldc2_w' : 3,
	'iinc' : 3,
	'ifeq' : 3,
	'ifne' : 3,
	'iflt' : 3,
	'ifge' : 3,
	'ifgt' : 3,
	'ifle' : 3,
	'if_icmpeq' : 3,
	'if_icmpne' : 3,
	'if_icmplt' : 3,
	'if_icmpge' : 3,
	'if_icmpgt' : 3,
	'if_icmple' : 3,
	'if_acmpeq' : 3,
	'if_acmpne' : 3,
	'goto' : 3,
	'jsr' : 3,
	'getstatic' : 3,
	'putstatic' : 3,
	'getfield' : 3,
	'putfield' : 3,
	'invokevirtual' : 3,
	'invokespecial' : 3,
	'invokestatic' : 3,
	'new' : 3,
	'anewarray' : 3,
	'checkcast' : 3,
	'instanceof' : 3,
	'ifnull' : 3,
	'ifnonnull' : 3,


	# 'tableswitch' : ?,
	# 'lookupswitch' : ?,
	'invokeinterface' : 5,
	'invokedynamic' : 5,
	# 'wide' : 3/5,
	'multianewarray' : 4,
	'goto_w' : 5,
	'jsr_w' : 5,

}



# list of instructions that reference constants
assemblyConstantReferenceListing = [
	'ldc',
	'ldc_w',
	'ldc2_w',
	'getstatic',
	'putstatic',
	'getfield',
	'putfield',
	'invokevirtual',
	'invokespecial',
	'invokestatic',
	'new',
	'anewarray',
	'checkcast',
	'instanceof',

	'multianewarray',
	'invokeinterface',
	'invokedynamic',
]


# list of instructions that jump execution
assemblyJumpListing = [
	'ifeq',
	'ifne',
	'iflt',
	'ifge',
	'ifgt',
	'ifle',
	'if_icmpeq',
	'if_icmpne',
	'if_icmplt',
	'if_icmpge',
	'if_icmpgt',
	'if_icmple',
	'if_acmpeq',
	'if_acmpne',
	'goto',
	'jsr',
	'ifnull',
	'ifnonnull',

	'goto_w',
	'jsr_w',
]

# list of jump instructions that always jump
assemblyAbsoluteJumpListing = [
	'goto',
	'jsr',
	'goto_w',
	'jsr_w',
]


# list of jump instructions that conditionally jump
assemblyConditionalJumpListing = [
	'ifeq',
	'ifne',
	'iflt',
	'ifge',
	'ifgt',
	'ifle',
	'if_icmpeq',
	'if_icmpne',
	'if_icmplt',
	'if_icmpge',
	'if_icmpgt',
	'if_icmple',
	'if_acmpeq',
	'if_acmpne',
	'ifnull',
	'ifnonnull',
]

assemblyAbsoluteLeaveListing = [
	'ireturn',
	'lreturn',
	'freturn',
	'dreturn',
	'areturn',
	'return',
	'athrow',
]




assemblyCriticalInstructionsListing = [
	'ldc',
	'ldc_w',
	'ldc2_w',

	'getstatic',
	'putstatic',
	'getfield',
	'putfield',
	'invokevirtual',
	'invokespecial',
	'invokestatic',
	'new',
	'anewarray',
	'checkcast',
	'instanceof',

	'multianewarray',
	'invokeinterface',
	'invokedynamic',

	'goto',
	'jsr',
	'goto_w',
	'jsr_w',
	'ireturn',
	'lreturn',
	'freturn',
	'dreturn',
	'areturn',
	'return',
	'return',
	'athrow',

	'ifeq',
	'ifne',
	'iflt',
	'ifge',
	'ifgt',
	'ifle',
	'if_icmpeq',
	'if_icmpne',
	'if_icmplt',
	'if_icmpge',
	'if_icmpgt',
	'if_icmple',
	'if_acmpeq',
	'if_acmpne',
	'ifnull',
	'ifnonnull',

	'tableswitch',
]



assemblyFieldReferencingListing = [
	'getstatic',
	'putstatic',
	'getfield',
	'putfield',
]

assemblyMethodReferencingListing = [
	'invokeinterface',
	'invokedynamic',
	'invokevirtual',
	'invokespecial',
	'invokestatic',
]



class ClassBytecode(object):
	def __init__(self, **kwargs):
		self.bytecode = b''
		self.assembly = []

		# these are options that only effect the stringing of bytecode, they have nothing to do with compiling/decompiling

		# labels bytecode offsets in each instruction
		self.labelOffsets = kwargs.get('labelOffsets', True)
		# # adds the bytecode offset to each jump instruction's argument to get the absolute destination
		# self.globalizeJumps = kwargs.get('globalizeJumps', True)
		# adds comments on the the constants referenced in assembly code by retrieving them from the given classfile
		self.resolveConstants = kwargs.get('resolveConstants', False)
		# calculates where jumps lead to and marks their destinations with helpful symbols about what jump types they are
		self.markJumpDestinations = kwargs.get('markJumpDestinations', True)
		self.markJumpSources = kwargs.get('markJumpSources', True)

		self.markExceptionRanges = kwargs.get('markExceptionRanges', True)
		# an exception table. if given and markJumpDestinations is enabled, it will use this to display exception handling locations
		self.exceptionTable = kwargs.get('exceptionTable', None)
		# classfile for resolving constants if resolveConstants is enabled
		self.classfile = kwargs.get('classfile', None)
	def decompile (self, bytecode):
		self.bytecode = bytecode
		offset = 0
		while offset < len(bytecode):
			c = bytecode[offset]
			if bytecode0ToAssembly.get(c) is not None:
				self.assembly.append(bytecode0ToAssembly[c])
				offset += 1
			elif bytecode1ToAssembly.get(c) is not None:
				self.assembly.append(bytecode1ToAssembly[c])
				self.assembly.append(struct.unpack('>B', bytecode[offset+1:offset+2])[0])
				offset += 2
			elif bytecode2ToAssembly.get(c) is not None:
				self.assembly.append(bytecode2ToAssembly[c])
				if bytecode2ToAssembly[c] == 'iinc':
					self.assembly.append(struct.unpack('>B', bytecode[offset+1:offset+2])[0])
					self.assembly.append(struct.unpack('>B', bytecode[offset+2:offset+3])[0])
				else:
					if bytecode2ToAssembly[c] in assemblyJumpListing:
						self.assembly.append(struct.unpack('>h', bytecode[offset+1:offset+3])[0])
					else:
						self.assembly.append(struct.unpack('>H', bytecode[offset+1:offset+3])[0])
				offset += 3
			elif bytecodeOtherToAssembly.get(c) is not None:
				instruction = bytecodeOtherToAssembly[c]
				if instruction == 'goto_w' or instruction == 'jsr_w':
					self.assembly.append(instruction)
					self.assembly.append(struct.unpack('>i', bytecode[offset+1:offset+5])[0])
					offset += 5
				elif instruction == 'invokedynamic':
					self.assembly.append(instruction)
					self.assembly.append(struct.unpack('>H', bytecode[offset+1:offset+3])[0])
					offset += 5
				elif instruction == 'invokeinterface':
					self.assembly.append(instruction)
					self.assembly.append(struct.unpack('>H', bytecode[offset+1:offset+3])[0])
					# this silly byte here serves no purpose and can be deducted from the method constant given
					# but it's too complex to recalculate it during packing that we just leave it
					self.assembly.append(struct.unpack('>B', bytecode[offset+3:offset+4])[0])
					offset += 5
				elif instruction == 'tableswitch':
					self.assembly.append(instruction)
					offset += 1
					if offset % 4 != 0:
						offset += 4 - offset % 4
					# print("offset:", offset)
					# print("padding:", padding)
					defaultGoto, low, high = struct.unpack('>iii', bytecode[offset:offset+12])
					offset += 12
					self.assembly.append(low)
					# print("data:", defaultGoto, low, high)
					# tableswitch is stored in a format of ['tableswitch', low, [*jump offsets*, default offset]]
					jumpOffsets = [ struct.unpack('>i', bytecode[offset+4*i:offset+4+4*i])[0] for i in range(high - low + 1) ]
					self.assembly.append(jumpOffsets + [defaultGoto])
					offset += (high - low + 1) * 4

				elif instruction == 'lookupswitch':
					self.assembly.append(instruction)
					offset += 1
					if offset % 4 != 0:
						offset += 4 - offset % 4
					# i have no clue why npairs can be signed, but it's in the spec for some reason
					defaultGoto, npairs = struct.unpack('>ii', bytecode[offset:offset+8])
					offset += 8
					# print('debug:', defaultGoto, npairs)
					# print(bytecode[offset+8*0:4+offset+8*0])
					# print(bytecode[4+offset+8*0:8+offset+8*0])lookupswitch
					# lookupswitch is stored in a format of ['lookupswitch', { keyn : jump offsetn, ..., 'default' : default offset }]
					jumpOffsets = { struct.unpack('>i', bytecode[offset+8*i:4+offset+8*i])[0] : struct.unpack('>i', bytecode[4+offset+8*i:8+offset+8*i])[0] \
							for i in range(npairs) }
					jumpOffsets['default'] = defaultGoto
					self.assembly.append(jumpOffsets)
					offset += npairs * 8

				elif instruction == 'multianewarray':
					self.assembly.append(instruction)
					self.assembly.append(struct.unpack('>H', bytecode[offset+1:offset+3])[0])
					self.assembly.append(struct.unpack('>B', bytecode[offset+3:offset+4])[0])
					offset += 4
				elif instruction == 'wide':
					self.assembly.append('wide')
					c2 = ord(bytecode[offset + 1])
					if c2 == 0x84: # iinc
						self.assembly.append('iinc')
						self.assembly.append(struct.unpack('>H', bytecode[offset+2:offset+4])[0])
						self.assembly.append(struct.unpack('>H', bytecode[offset+4:offset+6])[0])
						offset += 6
					elif bytecode1ToAssembly.get(c2) is not None:
						self.assembly.append(bytecode1ToAssembly[c2])
						self.assembly.append(struct.unpack('>H', bytecode[offset+2:offset+4])[0])
						offset += 4
					else:
						raise Exception('invalid wide bytecode:' + str(c))

				else:
					raise Exception('error')
			else:
				raise Exception('invalid bytecode:' + str(c))


	def compile(self, assembly=None):
		if assembly is None:
			assembly = self.assembly
		else:
			self.assembly = assembly

		index = 0
		bytecode = b''
		while index < len(assembly):
			if assemblyToBytecode.get(assembly[index]) is not None:
				code = assemblyToBytecode[assembly[index]]
				if bytecode0ToAssembly.get(code) is not None:
					bytecode += struct.pack('>B', code)
					index += 1
				elif bytecode1ToAssembly.get(code) is not None:
					bytecode += struct.pack('>BB', code, assembly[index + 1])
					index += 2
				elif bytecode2ToAssembly.get(code) is not None:
					if assembly[index] == 'iinc':
						bytecode += struct.pack('>BBB', code, assembly[index + 1], assembly[index + 2])
						index += 3
					elif assembly[index] in assemblyJumpListing:
						bytecode += struct.pack('>Bh', code, assembly[index + 1])
						index += 2
					else:
						bytecode += struct.pack('>BH', code, assembly[index + 1])
						index += 2
				elif bytecodeOtherToAssembly.get(code) is not None:
					if assembly[index] == 'goto_w' or assembly[index] == 'jsr_w':
						bytecode += struct.pack('>Bi', code, assembly[index + 1])
						index += 2
					elif assembly[index] == 'invokedynamic':
						bytecode += struct.pack('>BHBB', code, assembly[index + 1], 0 ,0)
						index += 2
					elif assembly[index] == 'invokeinterface':
						bytecode += struct.pack('>BHBB', code, assembly[index + 1], assembly[index + 2], 0)
						index += 3
					elif assembly[index] == 'tableswitch':
						bytecode += struct.pack('>B', code)
						if len(bytecode) % 4 != 0:
							bytecode += b'\x00' * (4 - len(bytecode) % 4) # padding
						jumpOffsets = assembly[index+2]
						bytecode += struct.pack('>iii', jumpOffsets[-1], assembly[index+1], assembly[index+1] + len(jumpOffsets) - 2)
						bytecode += struct.pack('>' + 'i' * (len(jumpOffsets) - 1), *jumpOffsets[:-1])
						index += 3
					elif assembly[index] == 'lookupswitch':
						bytecode += struct.pack('>B', code)
						if len(bytecode) % 4 != 0:
							bytecode += b'\x00' * (4 - len(bytecode) % 4) # padding
						jumpOffsets = assembly[index+1]
						bytecode += struct.pack('>ii', jumpOffsets['default'], len(jumpOffsets) - 1)
						for key in sorted([ key for key in jumpOffsets.keys() if type(key) == int ]):
							bytecode += struct.pack('>ii', key, jumpOffsets[key])
						index += 2
					elif assembly[index] == 'multianewarray':
						bytecode += struct.pack('>BHB', code, assembly[index + 1], assembly[index + 2]) 
						index += 3
					elif assembly[index] == 'wide':
						if assembly[index + 1] == 'iinc':
							bytecode += struct.pack('>BHH', assemblyToBytecode[assembly[index + 1]], assembly[index + 2], assembly[index + 3])
							index += 4
						else:
							bytecode += struct.pack('>BH', assemblyToBytecode[assembly[index + 1]], assembly[index + 2])
							index += 3
					else:
						raise Exception('invalid other assembly code for "'+str(assembly[index])+'" at index '+str(index))
				else:
					raise Exception('invalid assembly code for "'+str(assembly[index])+'" at index '+str(index))

			else:
				raise Exception('invalid assembly "'+str(assembly[index])+'" at index '+str(index))
		self.bytecode = bytecode

	def linkAssembly(self, classfile):
		offset = 0
		while offset < len(self.assembly):
			if type(self.assembly[offset]) == str and self.assembly[offset] in assemblyConstantReferenceListing:
				offset += 1
				self.assembly[offset] = classfile.constantFromIndex(self.assembly[offset])
			offset += 1

	# registers the linked assembly constants with a potentially foreign classfile
	# this allows transfer of assembly between classfiles
	def uninlineAssembly(self, classfile):
		offset = 0
		while offset < len(self.assembly):
			if type(self.assembly[offset]) == str and self.assembly[offset] in assemblyConstantReferenceListing:
				offset += 1
				self.assembly[offset] = classfile.getSetInlinedConstant(self.assembly[offset])
			offset += 1

	def unlinkAssembly(self, classfile):
		offset = 0
		while offset < len(self.assembly):
			if type(self.assembly[offset]) == str and self.assembly[offset] in assemblyConstantReferenceListing:
				offset += 1
				self.assembly[offset] = classfile.constantToIndex(self.assembly[offset])
			offset += 1

	def calculateJumpDestinations(self, assemblySearchList=assemblyJumpListing):
		jumpDestinations = {}

		offset = 0
		bytecodeOffset = 0
		while offset < len(self.assembly):
			if type(self.assembly[offset]) == str:
				if self.assembly[offset] in assemblySearchList:
					if self.assembly[offset] == 'tableswitch':
						for i in range(len(self.assembly[offset+2]) - 1):
							dest = self.assembly[offset+2][i] + bytecodeOffset
							if dest not in jumpDestinations:
								jumpDestinations[dest] = []
							jumpDestinations[dest].append(str(bytecodeOffset) + '[' + str(self.assembly[offset+1] + i) + ']')
						dest = self.assembly[offset+2][-1] + bytecodeOffset
						if dest not in jumpDestinations:
							jumpDestinations[dest] = []
						jumpDestinations[dest].append(str(bytecodeOffset) + '[default]')
					elif self.assembly[offset] == 'lookupswitch':
						jumpOffsets = self.assembly[offset+1]
						for key in sorted([ key for key in jumpOffsets.keys() if type(key) == int ]):
							dest = self.assembly[offset+1][key] + bytecodeOffset
							if dest not in jumpDestinations:
								jumpDestinations[dest] = []
							jumpDestinations[dest].append(str(bytecodeOffset) + '[' + str(key) + ']')
						dest = self.assembly[offset+1]['default'] + bytecodeOffset
						if dest not in jumpDestinations:
							jumpDestinations[dest] = []
						jumpDestinations[dest].append(str(bytecodeOffset) + '[default]')
					else:
						dest = self.assembly[offset+1] + bytecodeOffset
						if dest not in jumpDestinations:
							jumpDestinations[dest] = []
						jumpDestinations[dest].append(bytecodeOffset)

				bytecodeOffset += self.assemblyToSize(offset, bytecodeOffset)
				if self.assembly[offset] == 'wide':
					offset += 1
			offset += 1

		return jumpDestinations

	def calculateJumpSources(self, assemblySearchList=assemblyJumpListing):
		jumpSources = {}

		offset = 0
		bytecodeOffset = 0
		while offset < len(self.assembly):
			if type(self.assembly[offset]) == str:
				if self.assembly[offset] in assemblySearchList:
					if self.assembly[offset] == 'tableswitch':
						jumpSources[bytecodeOffset] = [ bytecodeOffset + dest for dest in self.assembly[offset+2] ]
					elif self.assembly[offset] == 'lookupswitch':
						jumpSources[bytecodeOffset] = [ bytecodeOffset + self.assembly[offset+1][key] for key in self.assembly[offset+1] ]
					else:
						jumpSources[bytecodeOffset] = [bytecodeOffset + self.assembly[offset+1]]


				bytecodeOffset += self.assemblyToSize(offset, bytecodeOffset)
				if self.assembly[offset] == 'wide':
					offset += 1
			offset += 1

		return jumpSources

	def calculateExceptionDestinations(self):
		jumpDestinations = {}

		for entry in self.exceptionTable:
			if entry['handler_pc'] not in jumpDestinations:
				jumpDestinations[entry['handler_pc']] = []
			jumpDestinations[entry['handler_pc']].append(entry)

		return jumpDestinations

	def calculateExceptionSources(self):
		jumpSources = {}

		for entry in self.exceptionTable:
			if entry['end_pc'] not in jumpSources:
				jumpSources[entry['end_pc']] = []
			jumpSources[entry['end_pc']].append(entry['handler_pc'])

		return jumpSources

	def calculateExceptionRanges(self):
		ranges = []

		for entry in self.exceptionTable:
			entry_comment = 'try [{}:{}] catch "{}" at {}'.format(entry['start_pc'], entry['end_pc'],
						classNameToCode(entry['catch_type']) if entry['catch_type'] is not None else '*', entry['handler_pc'])
			ranges.append([entry['start_pc'], entry['end_pc'], entry_comment, '* '])

		return ranges

	def detectLoopRanges(self):
		ranges = []
		jumpSources = self.calculateJumpSources(assemblyAbsoluteJumpListing)
		jumpDestinations = self.calculateJumpDestinations(assemblyConditionalJumpListing)
		for sourcepc in jumpSources:
			if jumpSources[sourcepc][0] < sourcepc:
				nextOffset = sourcepc + 3
				if nextOffset in jumpDestinations:
					possibleLoops = sorted([ jumpSource for jumpSource in jumpDestinations[nextOffset]\
							if jumpSources[sourcepc][0] <= jumpSource and jumpSource < sourcepc ])
					# print('checking for loop from {} ({}) : {}'.format(sourcepc, nextOffset, possibleLoops))
					if len(possibleLoops) > 0:
						ranges.append([ jumpSources[sourcepc][0], sourcepc,\
								'conditional loop [{}:{}] (exit at {})'.format(jumpSources[sourcepc][0], sourcepc, possibleLoops[0]), '| ' ])
		return ranges


	def isMethodFieldGetter(self):
		if len(self.assembly) == 4:
			if self.assembly[0] == 'aload_0' and self.assembly[1] == 'getfield':
				if self.assembly[3] == 'ireturn' or self.assembly[3] == 'lreturn' or self.assembly[3] == 'freturn' or self.assembly[3] == 'dreturn' or\
						self.assembly[3] == 'areturn':
					return True
		return False

	def isMethodFieldSetter(self):
		if len(self.assembly) == 5:
			if self.assembly[0] == 'aload_0' and self.assembly[2] == 'putfield' and self.assembly[4] == 'return':
				if self.assembly[1] == 'iload_1' or self.assembly[1] == 'lload_1' or self.assembly[1] == 'fload_1' or self.assembly[1] == 'dload_1' or\
						self.assembly[1] == 'aload_1':
					return True
		return False


	def stringAssembly(self, assemblyFilterList=None):
		code = ''

		if self.markJumpDestinations:
			tableJumpDestinations = self.calculateJumpDestinations(['tableswitch', 'lookupswitch'])
			absoluteJumpDestinations = self.calculateJumpDestinations(assemblyAbsoluteJumpListing)
			conditionalJumpDestinations = self.calculateJumpDestinations(assemblyConditionalJumpListing)
			if self.exceptionTable is not None:
				exceptionJumpDestinations = self.calculateExceptionDestinations()
			else:
				exceptionJumpDestinations = {}

		if self.markJumpSources:
			conditionalJumpSources = self.calculateJumpSources(assemblyConditionalJumpListing)
			absoluteJumpSources = self.calculateJumpSources(assemblyAbsoluteJumpListing)
			if self.exceptionTable is not None:
				exceptionJumpSources = self.calculateExceptionSources()
			else:
				exceptionJumpSources = {}

		rangesProcessed = []
		rangesProcessed += self.detectLoopRanges()
		if self.markExceptionRanges and self.exceptionTable is not None:
			rangesProcessed += self.calculateExceptionRanges()



		postLineInfo = {}
		preLineInfo = {}

		# process outgoing jumps
		if self.markJumpSources:
			for offset in absoluteJumpSources:
				if offset not in postLineInfo:
					postLineInfo[offset] = []
				postLineInfo[offset].append( str(offset) +' >>-- ' + ', '.join( str(pc) for pc in absoluteJumpSources[offset] ) )
				postLineInfo[offset].append('')
			for offset in conditionalJumpSources:
				if offset not in postLineInfo:
					postLineInfo[offset] = []
				postLineInfo[offset].append( str(offset) +' >>?? ' + ', '.join( str(pc) for pc in conditionalJumpSources[offset] ) )
			for offset in exceptionJumpSources:
				if offset not in postLineInfo:
					postLineInfo[offset] = []
				postLineInfo[offset].append( str(offset) +' >>** ' + ', '.join( str(pc) for pc in exceptionJumpSources[offset] ) )

		# process incoming jumps
		if self.markJumpDestinations:
			for offset in exceptionJumpDestinations:
				if offset not in preLineInfo:
					preLineInfo[offset] = []
				preLineInfo[offset].append( str(offset) + ' <<** ' + ','.join(\
					'[{}:{}] : {}'.format(entry['start_pc'], entry['end_pc'], str(classNameToCode(entry['catch_type']) if entry['catch_type'] is not None else '*')) \
						for entry in exceptionJumpDestinations[offset] \
				) )
			for offset in tableJumpDestinations:
				if offset not in preLineInfo:
					preLineInfo[offset] = []
				preLineInfo[offset].append( str(offset) + ' <<## ' + ','.join(str(source) for source in tableJumpDestinations[offset]) )
			for offset in absoluteJumpDestinations:
				if offset not in preLineInfo:
					preLineInfo[offset] = []
				preLineInfo[offset].append( str(offset) + ' <<-- ' + ','.join(str(source) for source in absoluteJumpDestinations[offset]) )
			for offset in conditionalJumpDestinations:
				if offset not in preLineInfo:
					preLineInfo[offset] = []
				preLineInfo[offset].append( str(offset) + ' <<?? ' + ','.join(str(source) for source in conditionalJumpDestinations[offset]) )




		if self.isMethodFieldGetter():
			if 0 not in preLineInfo:
				preLineInfo[0] = []
			preLineInfo[0].append('// field getter method')
		if self.isMethodFieldSetter():
			if 0 not in preLineInfo:
				preLineInfo[0] = []
			preLineInfo[0].append('// field setter method')

		offset = 0
		bytecodeOffset = 0
		lastBytecodeOffset = bytecodeOffset - 1
		lastInstruction = None

		activeRangeStack = []
		markRange = ''
		while offset < len(self.assembly):
			if type(self.assembly[offset]) == str:

				if len(code) != 0 and (assemblyFilterList is None or lastInstruction in assemblyFilterList):
					code += '\n'

				# process outgoing jumps
				if self.markJumpSources:
					if lastInstruction is not None and lastInstruction in assemblyAbsoluteLeaveListing:
						code += '\t' + markRange + str(lastBytecodeOffset) +' >>-->>\n' + '\t' + markRange + '\n'

				#display post-line info
				if lastBytecodeOffset in postLineInfo:
					for line in postLineInfo[lastBytecodeOffset]:
						code += '\t' + markRange + line + '\n'


				# purge ranges
				oldRanges = activeRangeStack
				activeRangeStack = [ activeRange for activeRange in activeRangeStack if activeRange[0] <= bytecodeOffset and bytecodeOffset <= activeRange[1] ]
				markRange = ''.join( activeRange[3] for activeRange in activeRangeStack )
				if len(activeRangeStack) != len(oldRanges):
					code += '\t' + markRange + '\n'

				# process additional ranges
				for displayedRange in rangesProcessed:
					if displayedRange[0] == bytecodeOffset:
						code += '\t' + markRange + '# ' + displayedRange[2] + '\n'
						activeRangeStack.append(displayedRange)

				markRange = ''.join( activeRange[3] for activeRange in activeRangeStack )

				#display pre-line info
				if bytecodeOffset in preLineInfo:
					for line in preLineInfo[bytecodeOffset]:
						code += '\t' + markRange + line + '\n'


				# display the instruction
				if self.assembly[offset] == 'wide':
					inst = 'wide ' + self.assembly[offset+1]
					lastInstruction = self.assembly[offset+1]
				else:
					inst = self.assembly[offset]
					lastInstruction = inst

				if self.labelOffsets and (assemblyFilterList is None or lastInstruction in assemblyFilterList):
					code += str(bytecodeOffset) + ':\t' + markRange + '\t'

				if assemblyFilterList is None or lastInstruction in assemblyFilterList:
					code += inst

				# increment offsets
				lastBytecodeOffset = bytecodeOffset
				bytecodeOffset += self.assemblyToSize(offset, bytecodeOffset)
				if self.assembly[offset] == 'wide':
					offset += 1
			else:
				if assemblyFilterList is None or lastInstruction in assemblyFilterList:
					if lastInstruction in assemblyJumpListing:
						code += ' ' + str(self.assembly[offset] + lastBytecodeOffset)
					elif self.resolveConstants and type(self.assembly[offset-1]) == str and lastInstruction in assemblyConstantReferenceListing:
						code += ' #' + str(self.assembly[offset]) + '\t\t// ' +\
								stringConstantSimple(self.classfile.constantFromIndex(self.assembly[offset]))
					elif type(self.assembly[offset-1]) == str and lastInstruction == 'tableswitch':
						code += ' (' + str(self.assembly[offset]) + ' .. ' + str(self.assembly[offset] + len(self.assembly[offset+1]) - 2) + ')'
					elif type(self.assembly[offset-2]) == str and lastInstruction == 'tableswitch':
						code += ' {\n'
						for i in range(len(self.assembly[offset]) - 1):
							code += '\t' + str(self.assembly[offset-1] + i) + ': ' + str(self.assembly[offset][i] + lastBytecodeOffset) + '\n'
						code += '\tdefault: ' + str(self.assembly[offset][-1] + lastBytecodeOffset) + '\n'
						code += '}'
					elif type(self.assembly[offset-1]) == str and lastInstruction == 'lookupswitch':
						code += ' {\n'
						for key in sorted([ key for key in self.assembly[offset].keys() if type(key) == int ]):
							code += '\t' + str(key) + ': ' + str(self.assembly[offset][key] + lastBytecodeOffset) + '\n'
						code += '\tdefault: ' + str(self.assembly[offset]['default'] + lastBytecodeOffset) + '\n'
						code += '}'
					else:
						if isinstance(self.assembly[offset], classfile.ClassFileConstant):
							code += ' ' + stringConstantSimple(self.assembly[offset])
						else:
							code += ' ' + str(self.assembly[offset])
			offset += 1

		return code

	def assemblyToSize(self, offset, bytecodeOffset):
		if assemblyToSizeTable.get(self.assembly[offset]) is not None:
			return assemblyToSizeTable[self.assembly[offset]]
		elif self.assembly[offset] == 'wide':
			if self.assembly[offset + 1] == 'iinc':
				return 5
			else:
				return 3
		elif self.assembly[offset] == 'tableswitch':
			padding = 4 - bytecodeOffset % 4
			return padding + len(self.assembly[offset+2]) * 4 + 8
		elif self.assembly[offset] == 'lookupswitch':
			padding = 4 - bytecodeOffset % 4
			return padding + len(self.assembly[offset+1]) * 8
		else:
			raise Exception('unknown assembly: '+self.assembly[offset])






def decompileAndLink(bytecode, classfile):
	bc = ClassBytecode()
	bc.decompile(bytecode)
	bc.linkAssembly(classfile)

	return bc.assembly


def unlinkAndCompile(assembly, classfile):
	bc = ClassBytecode()
	bc.assembly = assembly
	# uninline the assembly to ensure that the constants are present
	bc.uninlineAssembly(classfile)
	# relink and recompile the bytecode
	bc.unlinkAssembly(classfile)
	bc.compile()

	return bc.bytecode



if __name__ == '__main__':
	bc = ClassBytecode()
	bc.decompile(b'\xb2\x00\x02\x12\x03\xb6\x00\x04\xa7\x00\x0cL\xb2\x00\x02\x12\x06\xb6\x00\x04\xb1')
	print (bc.assembly)
	bc.compile()
	print ([b'\xb2\x00\x02\x12\x03\xb6\x00\x04\xa7\x00\x0cL\xb2\x00\x02\x12\x06\xb6\x00\x04\xb1'])
	print ([bc.bytecode])
	print (bc.stringAssembly())
