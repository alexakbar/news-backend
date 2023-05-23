<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/

// set up the routes for the API
Route::group(['prefix' => 'v1'], function () {
    Route::post('/register', [App\Http\Controllers\API\AuthController::class, 'register'])->name('register');
    Route::post('login', [App\Http\Controllers\API\AuthController::class, 'login'])->name('login');

    Route::get('categories', [App\Http\Controllers\API\CategoryController::class, 'getCategories'])->name('getCategories');
    Route::get('sources', [App\Http\Controllers\API\SourceController::class, 'getSources'])->name('getSources');
    Route::get('authors', [App\Http\Controllers\API\AuthorController::class, 'getAuthors'])->name('getAuthors');

    Route::group(['middleware' => 'auth:api'], function () {
        Route::get('logout', [App\Http\Controllers\API\AuthController::class, 'logout'])->name('logout');
        Route::get('user', [App\Http\Controllers\API\UserController::class, 'getUser'])->name('getUser');
        Route::post('set-personalize', [App\Http\Controllers\API\UserController::class, 'setPersonalize'])->name('setPersonalize');
        Route::post('search-articles', [App\Http\Controllers\API\ArticlesController::class, 'searchArticles'])->name('searchArticles');
    });

});
