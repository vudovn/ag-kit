---
name: flutter-workspace-patterns
description: The exact architectural, state management, and UI patterns used across the flutter_resident and flutter_pkg_* monorepo workspace.
version: 1.0.0
---

# Flutter Workspace Patterns (The "Golden Knowledge Base")

**Purpose**: This skill contains the explicit codebase rules and existing patterns found in the user's `flutter_resident` and `flutter_pkg_*` monorepo. **ALL Flutter agents (especially `flutter-expert`) MUST adhere to these rules when writing code for this workspace.**

## 1. State Management (Provider & ChangeNotifier)
The workspace strictly uses the `Provider` package with `ChangeNotifier` for state management. 

### Provider Rules:
- **Class Structure**: Use `class FeatureProvider extends ChangeNotifier`.
- **Loading State**: Maintain explicit `_isLoading` flags (e.g., `bool _isLoading = true; bool get isLoading => _isLoading;`).
- **Error State**: Maintain `_errorMessage` properties (e.g., `String? _errorMessage; String? get errorMessage => _errorMessage;`).
- **Data Access**: Cross-provider data access is common (e.g., passing a `RunwalMyAccountProvider` into a child provider to read `.bookingDetail`).
- **Repository Injection**: Instantiate the specific repository interface at the top of the provider (e.g., `final IFeatureRepository _repository = FeatureRepository();`).

## 2. Repository Layer (API Calls)
The `repository` layer is strictly separated from the `provider` layer.

### Repository Rules:
- **Interfaces**: Always define an interface `IFeatureRepository` and implement it in `FeatureRepository`.
- **API Endpoints**: Kept in static string classes like `RunwalEndpoints` or `EndPoints` (e.g., `RunwalEndpoints.downloadPdfReceipt`).
- **Tokens**: Bearer tokens are fetched asynchronously right before the call (e.g., `final token = await RunwalPrefs.getSfdcToken();`). Check for null/empty token before making requests.
- **HTTP Client**: Use the standard `http` package (`import 'package:http/http.dart' as http;`).
- **JSON Decoding**: `jsonDecode(response.body)` is standard.
- **Errors**: Return `null` or throw caught exceptions on failure. Log errors using `logError` rather than printing.

## 3. Custom UI Widgets & Helpers
The workspace heavily leverages the `flutter_pkg_panchshil_widgets` package for unified UI and utilities.

### UI Helper Rules:
- **Logging**: Do NOT use `print()`. Use `logInfo(msg: "...")` and `logError(msg: "...")` from `package:flutter_pkg_panchshil_widgets/utils/custom_logger.dart`.
- **Toasts**: Use `toastDialog(msg: '...', toastGravity: ToastGravity.BOTTOM);` from `package:flutter_pkg_panchshil_widgets/utils/toast_dialog.dart`.
- **Loading Dialogs (nDialog)**: Use `CustomProgressDialog pd = loadingPleaseWaitDialog(context: context); pd.show();` and `pd.dismiss();` from `package:flutter_pkg_panchshil_widgets/widgets/common/loading_dialog.dart`.
- **PDF Viewer**: Use `Base64PdfViewerScreen` from `package:flutter_pkg_panchshil_widgets/widgets/common/base_64_pdf_view_screen.dart`.

## 4. Multi-Package Architecture
- When building features, check which package they belong to (e.g., `flutter_pkg_panchshil_my_account`, `resident_post_sales_referral_pkg`, etc.). 
- Do NOT import code from `flutter_resident` into a package. Packages should be independent or only rely on `flutter_pkg_panchshil_widgets` for shared utilities.

## Checklist for Agents
- [ ] Are logs using `logInfo` and `logError`?
- [ ] Are API endpoints pulled from `EndPoints`/`RunwalEndpoints`?
- [ ] Is State Management using `ChangeNotifier` and properly handling `isLoading`?
- [ ] Is the code correctly avoiding circular dependencies between the packages?
