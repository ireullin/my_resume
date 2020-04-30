package helpers

import freemarker.template.Configuration
import freemarker.template.TemplateExceptionHandler
import java.io.StringWriter


class Html(name:String){

    companion object{
        private val cfg = Configuration(Configuration.VERSION_2_3_22).apply {
            setClassForTemplateLoading(this.javaClass, "/views")
            setDefaultEncoding("UTF-8")
            setTemplateExceptionHandler(TemplateExceptionHandler.RETHROW_HANDLER)
        }
    }

    private val tmp = cfg.getTemplate(name)

    fun render(vararg data:Pair<*,*>):String{
        val stringWriter = StringWriter()
        tmp.process(data.toMap(), stringWriter)
        return stringWriter.toString()
    }

    fun render(data:Map<*,*>):String{
        val stringWriter = StringWriter()
        tmp.process(data.toMap(), stringWriter)
        return stringWriter.toString()
    }

    fun render():String{
        val stringWriter = StringWriter()
        tmp.process(mapOf<String,String>(), stringWriter)
        return stringWriter.toString()
    }
}