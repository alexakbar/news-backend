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
    Route::group(['middleware' => 'auth:api'], function () {
        Route::get('logout', [App\Http\Controllers\API\AuthController::class, 'logout'])->name('logout');
        Route::get('user', [App\Http\Controllers\API\UserController::class, 'getUser'])->name('getUser');
    });

});
