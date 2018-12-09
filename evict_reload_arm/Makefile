CC_ARM=$(NDK)/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/bin/arm-linux-androideabi-gcc
CC_AARCH64=$(NDK)/toolchains/aarch64-linux-android-4.9/prebuilt/linux-x86_64/bin/aarch64-linux-android-gcc
SYSROOT_ARM=$(NDK)/platforms/android-23/arch-arm
SYSROOT_AARCH64=$(NDK)/platforms/android-23/arch-arm64

arm:
	$(CC_ARM) -O0 $(CFLAGS) -D _GNU_SOURCE -w -std=gnu99 --sysroot=$(SYSROOT_ARM) -march=armv8-a -fPIE -marm -o arm_fnr main.c -ldl -pie

aarch64:
	$(CC_AARCH64) $(CFLAGS) -D _GNU_SOURCE -w -std=gnu99 --sysroot=$(SYSROOT_AARCH64) -march=armv8-a -fPIE -o arm_fnr main.c -ldl -pie

clean:
	rm arm_fnr
