import controllers.Example
import controllers.Resume
import io.ktor.application.*
import io.ktor.http.content.resources
import io.ktor.http.content.static
import io.ktor.routing.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*

fun main(args:Array<String>) {
    embeddedServer(Netty, 1234) {
        routing {
            get("/{lang}/short"){Resume(call).short()}
            get("/{lang}/full"){ Resume(call).full()}

            route("/echo"){
                get("/"){Example(call).echo()}
                get("/{name}"){Example(call).echoWithId()}
                post("/"){Example(call).echoFromPost()}
            }

            // url上面遇到assets就去resources裡頭找assets
            static("assets"){
                resources("assets")
            }
      }
   }.start(wait = true)

}
