import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:university_assignment_manager/core/theme/theme_controller.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUp(() {
    SharedPreferences.setMockInitialValues({});
    ThemeController.mode.value = ThemeMode.system;
  });

  test('loads saved dark mode on initialize', () async {
    SharedPreferences.setMockInitialValues({'theme_mode': 'dark'});

    await ThemeController.initialize();

    expect(ThemeController.mode.value, ThemeMode.dark);
  });

  test('toggleLightDark persists updated value', () async {
    await ThemeController.initialize();

    await ThemeController.toggleLightDark();

    expect(ThemeController.mode.value, ThemeMode.dark);

    final prefs = await SharedPreferences.getInstance();
    expect(prefs.getString('theme_mode'), 'dark');
  });

  test('setSystemMode persists system mode', () async {
    SharedPreferences.setMockInitialValues({'theme_mode': 'dark'});
    await ThemeController.initialize();

    await ThemeController.setSystemMode();

    expect(ThemeController.mode.value, ThemeMode.system);

    final prefs = await SharedPreferences.getInstance();
    expect(prefs.getString('theme_mode'), 'system');
  });

  test('setLightMode persists light mode', () async {
    SharedPreferences.setMockInitialValues({'theme_mode': 'dark'});
    await ThemeController.initialize();

    await ThemeController.setLightMode();

    expect(ThemeController.mode.value, ThemeMode.light);

    final prefs = await SharedPreferences.getInstance();
    expect(prefs.getString('theme_mode'), 'light');
  });

  test('setDarkMode persists dark mode', () async {
    SharedPreferences.setMockInitialValues({'theme_mode': 'light'});
    await ThemeController.initialize();

    await ThemeController.setDarkMode();

    expect(ThemeController.mode.value, ThemeMode.dark);

    final prefs = await SharedPreferences.getInstance();
    expect(prefs.getString('theme_mode'), 'dark');
  });
}
