<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->string('preferred_sources')->nullable()->after('email');
            $table->string('categories')->nullable()->after('preferred_sources');
            $table->string('authors')->nullable()->after('categories');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::table('users', function (Blueprint $table) {
            // drop
            $table->dropColumn('preferred_sources');
            $table->dropColumn('categories');
            $table->dropColumn('authors');
        });
    }
};
