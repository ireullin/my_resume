package controllers

import helpers.Html
import io.ktor.application.ApplicationCall
import io.ktor.http.ContentType
import io.ktor.request.receiveText
import io.ktor.response.respondText

class Example(val call:ApplicationCall){
    suspend fun index(){
        call.respondText("fuck root", ContentType.Text.Html)
    }

    suspend fun echo(){
        call.respondText("fuck echo", ContentType.Text.Html)
    }

    suspend fun echoWithId(){
        val name = call.parameters["name"]
        val html = Html("/example/index.ftl").render("name" to name, "age" to 30)
        call.respondText(html,ContentType.Text.Html)
    }

    suspend fun echoFromPost(){
        val body = call.receiveText()
        call.respondText("fuck $body",ContentType.Text.Html)
    }
}